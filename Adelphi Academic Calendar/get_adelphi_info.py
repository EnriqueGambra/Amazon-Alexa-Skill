import urllib.request
import json
import re


class AdelphiInfo:
    """Class that will create a JSON file full of Adelphi academic calendar information."""

    def __init__(self):
        """Initializes the class."""
        self.url = "https://registrar.adelphi.edu/academic-calendar/"
        self.filename = "tmp/calendar_data.txt"
        self.filename_json = "tmp/adelphi_calendar.json"
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
        more_parsed = list()
        for element in data:
            data_parsed = element.strip()
            more_refined = data_parsed.replace("\\", "")
            even_more_refined = more_refined.replace("n'b'", "")
            clean = even_more_refined.strip()
            more_parsed.append(clean)       # Appended to an even more refined list

        # Create two lists, one for dates and the other for events
        dates = list()
        events = list()

        # Go through the more_parsed list, find elements that start with a month and append it to the dates list
        # And then the next index in the list should be an event, so append it into the events list
        for index in range(len(more_parsed)):
            if more_parsed[index].startswith("January") or more_parsed[index].startswith("February") or more_parsed[index].startswith("March")\
                    or more_parsed[index].startswith("April") or more_parsed[index].startswith("May") or more_parsed[index].startswith("June")\
                    or more_parsed[index].startswith("July") or more_parsed[index].startswith("August") or more_parsed[index].startswith("September")\
                    or more_parsed[index].startswith("October") or more_parsed[index].startswith("November") or more_parsed[index].startswith("December"):
                dates.append(more_parsed[index])
                events.append(more_parsed[index+1])

        dates_with_year = list()  # Creates a new list that will have the dates with year
        year = 2019     # The year we start at, 2019 needs to be fixed where it allows the program to be reusable, but for now its hardcoded in
        is_new_year = False
        # Appends the proper dates to each month
        for date in dates:
            if date.startswith("January") and is_new_year is False:
                year += 1
                is_new_year = True
            elif date.startswith("January") and is_new_year is True:
                pass
            else:
                is_new_year = False
            dates_with_year.append(f'{date} {year}')

        date_events_dict = dict()
        # Creates a dictionary, each date is a key, and each event is a value corresponding to that key

        for index in range(len(dates_with_year)):
            date_events_dict[events[index]] = dates_with_year[index]

        with open(self.filename_json, 'w') as f:
            json.dump(date_events_dict, f, indent=4)
