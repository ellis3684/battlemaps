from math import radians, cos, sin, asin, sqrt
import pprint
import json

battles = json.loads(open("battle_map_data.json").read())

test_lat = 0
test_long = -165


def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) -- this utilizes the haversine formula
    """
    # convert decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    # haversine formula
    longitude_difference = long2 - long1
    latitude_difference = lat2 - lat1
    a = sin(latitude_difference / 2) ** 2 + cos(lat1) * cos(lat2) * sin(longitude_difference / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km


battle_list = sorted(battles, key=lambda d: dist(test_lat, test_long, float(d["latitude"]), float(d["longitude"])))
pprint.pprint(battle_list[:5])
