import urllib.request
import json
import re


class AdelphiInfo:
    """Class that will create a JSON file full of Adelphi academic calendar information."""

    def __init__(self):
        """Initializes the class."""
        self.url = "https://registrar.adelphi.edu/academic-calendar/"
        self.filename = "data/calendar_data.txt"
        self.filename_json = "data/adelphi_calendar.json"
        self.create_text_file()

    def create_text_file(self):
        """Creates a text file."""
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        with open(self.filename, 'w') as f:
            for line in urllib.request.urlopen(self.url):
                cleantext = re.sub(cleanr, '', str(line))
                f.write(cleantext)

        with open(self.filename) as f:
            line = f.readline()
            data = line.split("\\t")

        parsed_data = list()
        for element in data:
            if element.startswith(' '):
                parsed_data.append(element)

        self.create_json_file(parsed_data)

    def create_json_file(self, data):
        """Creates the JSON file"""
        more_parsed = list()
        for element in data:
            data_parsed = element.strip()
            more_refined = data_parsed.replace("\\", "")
            even_more_refined = more_refined.replace("n'b'", "")
            clean = even_more_refined.strip()
            more_parsed.append(clean)

        dates = list()
        events = list()

        for index in range(len(more_parsed)):
            if more_parsed[index].startswith("January") or more_parsed[index].startswith("February") or more_parsed[index].startswith("March")\
                    or more_parsed[index].startswith("April") or more_parsed[index].startswith("May") or more_parsed[index].startswith("June")\
                    or more_parsed[index].startswith("July") or more_parsed[index].startswith("August") or more_parsed[index].startswith("September")\
                    or more_parsed[index].startswith("October") or more_parsed[index].startswith("November") or more_parsed[index].startswith("December"):
                dates.append(more_parsed[index])
                events.append(more_parsed[index+1])

        dates_with_year = list()
        year = 2019
        is_new_year = False
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

        for index in range(len(dates_with_year)):
            date_events_dict[dates_with_year[index]] = events[index]

        with open(self.filename_json, 'w') as f:
            json.dump(date_events_dict, f, indent=4)
