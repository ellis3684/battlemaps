# Convert csv to json for use with Django project

import csv
import json

csv_battles = "battles_with_coords_as_floats.csv"
json_battles = "battle_map_data.json"

with open(csv_battles, "r", newline="", encoding="utf-8") as file:
    battles = list(csv.DictReader(file))


with open(json_battles, "w", newline="", encoding="utf-8") as new_file:
    json.dump(battles, new_file, indent=2)
