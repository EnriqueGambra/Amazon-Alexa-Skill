from datetime import date
from datetime import timedelta
import json

filename = "tmp/adelphi_calendar2.json"
today = date.today()
event = "matriculation day"

with open(filename) as f:
    calendar_info_dict = json.load(f)

future_date = calendar_info_dict[event]
month_day_year = future_date.split(" ")

month_num_dict = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

month = month_num_dict.get(month_day_year[0])
day = month_day_year[1]
year = month_day_year[2]

# future = date(int(year), month, int(day))
# print(future)
# days_until = future - today
# print(days_until)
# if(str(days_until).find('-')) is not -1:
#     print("event passed")

num_month_dict = {
    '01': 'january',
    '02': 'february',
    '03': 'march',
    '04': 'april',
    '05': 'may',
    '06': 'june',
    '07': 'july',
    '08': 'august',
    '09': 'september',
    '10': 'october',
    '11': 'november',
    '12': 'december'
}

date_event_dict = dict()
for key, value in calendar_info_dict.items():
    date_event_dict[value] = key

# print(date_event_dict)
day_counter = 0
while True:
    next_date = today + timedelta(days=day_counter)
    year_month_day = str(next_date).split("-")
    year = year_month_day[0]
    month = year_month_day[1]
    day = year_month_day[2]

    converted_date = f'{num_month_dict.get(month)} {day} {year}'
    if converted_date in date_event_dict:
        next_event = date_event_dict[converted_date]
        break
    elif int(year) > 2024:
        break
    day_counter += 1

print(next_event)


event_date = calendar_info_dict['spring break']
event_date_list = event_date.split('-')
month_day = event_date_list[0]
year = event_date[len(event_date) - 4:]
month_day_year = month_day + " " + year
print(month_day_year)
