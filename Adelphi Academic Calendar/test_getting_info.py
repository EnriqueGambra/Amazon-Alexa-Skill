from get_adelphi_info import AdelphiInfo
import json
create_json = AdelphiInfo()

filename = "tmp/adelphi_calendar.json"

calendar_info_dict = dict()
with open(filename) as f:
    calendar_info_dict = json.load(f)

