import urllib.request
import json
import re


class AdelphiInfo:
    """Class that will create a JSON file full of Adelphi academic calendar information."""

    def __init__(self):
        """Initializes the class."""
        self.url = "https://registrar.adelphi.edu/academic-calendar/"
        self.filename = "tmp/calendar_data.txt"
        self.filename_json = "tmp/adelphi_calendar2.json"
        self.create_text_file()

    def create_text_file(self):
        """Creates a text file. Then passes the parsed_data list so it can create a json file."""
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        with open(self.filename, 'w') as f:
            for line in urllib.request.urlopen(self.url):
                cleantext = re.sub(cleanr, '', str(line))   # Cleans up text with regex and eliminates html code
                f.write(cleantext)  # Writes to the text file

        with open(self.filename) as f:
            line = f.readline()     # Opens the text file and starts splitting into a list based on '//t'
            data = line.split("\\t")

        parsed_data = list()
        for element in data:
            if element.startswith(' '):     # Parses tmp even more
                parsed_data.append(element)     # Appends to the parsed_data

        self.create_json_file(parsed_data)

    def create_json_file(self, data):
        """Creates the JSON file"""
        # Cleans up the code even more, getting rid of whitespace, double // and other strings
        more_parsed = self._clean_up_text(data)

        dates = list()
        events = list()

        # Go through the more_parsed list, find elements that start with a month and append it to the dates list
        # And then the next index in the list should be an event, so append it into the events list
        for index in range(len(more_parsed)):
            if more_parsed[index].startswith("january") or more_parsed[index].startswith("february") or more_parsed[index].startswith("march")\
                    or more_parsed[index].startswith("april") or more_parsed[index].startswith("may") or more_parsed[index].startswith("june")\
                    or more_parsed[index].startswith("july") or more_parsed[index].startswith("august") or more_parsed[index].startswith("september")\
                    or more_parsed[index].startswith("october") or more_parsed[index].startswith("november") or more_parsed[index].startswith("december"):
                dates.append(more_parsed[index])
                events.append(more_parsed[index+1])

        dates_with_year = self._combine_dates_with_year(dates) # Calls upon the dates_with_year helper method

        date_events_dict = self._combine_date_events(dates_with_year, events)

        # Create the JSON file
        with open(self.filename_json, 'w') as f:
            json.dump(date_events_dict, f, indent=4)

    def _clean_up_text(self, data):
        """Cleans up the text more, gets rid of backslashes and other html encodings"""
        more_parsed = list()
        for element in data:
            data_parsed = element.strip()
            more_refined = data_parsed.replace("\\", "")
            even_more_refined = more_refined.replace("n'b'", "")
            clean = even_more_refined.strip()
            clean = clean.lower()
            more_parsed.append(clean)       # Appended to an even more refined list

        return more_parsed

    def _combine_dates_with_year(self, dates):
        """Helper method that will combine the dates with the year"""
        # Create two lists, one for dates and the other for events

        dates_with_year = list()  # Creates a new list that will have the dates with year
        year = 2019     # The year we start at, 2019 needs to be fixed where it allows the program to be reusable, but for now its hardcoded in
        is_new_year = False
        # Appends the proper dates to each month
        for date in dates:
            if date.startswith("january") and is_new_year is False:
                year += 1
                is_new_year = True
            elif date.startswith("january") and is_new_year is True:
                pass
            else:
                is_new_year = False
            dates_with_year.append(f'{date} {year}')

        return dates_with_year

    def _combine_date_events(self, dates_with_year, events):
        """Helper method that creates a dictionary with each event corresponding to correct date"""
        date_events_dict = dict()

        semesters = ['fall 2019', 'spring 2020']
        count = 0
        # Creates a dictionary, each date is a key, and each event is a value corresponding to that key
        for index in range(len(dates_with_year)):
            key = events[index].replace("-", "for")
            if key == 'finals begin' or key == 'finals end':  # Replaces the - with for
                if count < 2:
                    updated_key = key + " for " + semesters[0]
                    count += 1
                else:
                    updated_key = key + " for " + semesters[1]
                    count += 1
                date_events_dict[updated_key] = dates_with_year[index]
            elif key.find(" i ") is not -1 or key.find(" ii ") is not -1:  # Replaces the ii with first term or second term
                if key.find(" i ") is not -1:
                    updated_key = key.replace(" i ", " first term ")
                elif key.find(" ii ") is not -1:
                    updated_key = key.replace(" ii ", " second term ")
                date_events_dict[updated_key] = dates_with_year[index]
            elif key.find("/") is not -1:
                updated_key = key.replace("/", " or ")
                date_events_dict[updated_key] = dates_with_year[index]
            elif key.find("for no classes") is not -1:
                updated_key = key.replace("for no classes", "")
                updated_key = updated_key.strip()
                date_events_dict[updated_key] = dates_with_year[index]
            else:
                date_events_dict[key] = dates_with_year[index]

            new_dict = self._replace_first_1st(date_events_dict)  # Replaces first with 1st

        return new_dict

    def _replace_first_1st(self, date_events_dict):
        """Helper method that will replace keys with the word first with 1st"""
        for key in date_events_dict.keys():
            if key.find("first") is not -1:
                new_key = key.replace("first", "1st")
                date_events_dict[new_key] = date_events_dict[key]
                del date_events_dict[key]

        return date_events_dict
