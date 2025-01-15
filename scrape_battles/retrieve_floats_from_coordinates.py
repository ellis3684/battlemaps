import csv


def is_west_or_is_south(coords_to_check):
    """Check if lat/lng is in western hemisphere or southern hemisphere"""
    if "W" in coords_to_check or "S" in coords_to_check:
        return True
    return False


def get_float(lat_or_lng):
    """Get floating point number for coordinates scraped from Wikipedia"""
    if is_west_or_is_south(lat_or_lng):
        return float(''.join(num for num in lat_or_lng if (num.isdigit() or num == '.'))) * -1
    return float(''.join(num for num in lat_or_lng if (num.isdigit() or num == '.')))


with open('battles_with_coords.csv', 'r', newline='', encoding='utf-8') as file:
    battles = list(csv.DictReader(file))

    # for index, battle in enumerate(battles):
    #     coords = battle['coordinates']
    #     battle_name = battle['battle']
    #     coord_sub_list = coords.split()

# checking for coordinates in csv that may have come out incorrectly from web scraping
#         if len(coord_sub_list) != 2:
#             print(f"{index}: {battle_name}")

#         lat = get_float(coord_sub_list[0])
#         lng = get_float(coord_sub_list[1])


# check for values greater than 90 for latitude, or greater than 180 for longitude
#         if lat >= 90 or lng >= 180:
#             print(f"{index}: {battle_name} at {coords}")


with open('battles_with_coords_as_floats.csv', 'w', newline='', encoding='utf-8') as new_file:
    fieldnames = ['battle', 'link', 'date', 'latitude', 'longitude']
    writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    writer.writeheader()
    for battle in battles:
        coords = battle['coordinates']
        battle_name = battle['battle']
        battle_url = battle['link']
        battle_date = battle['date']
        coord_sub_list = coords.split()
        lat = get_float(coord_sub_list[0])
        lng = get_float(coord_sub_list[1])
        writer.writerow({
            'battle': battle_name,
            'link': battle_url,
            'date': battle_date,
            'latitude': lat,
            'longitude': lng
        })


