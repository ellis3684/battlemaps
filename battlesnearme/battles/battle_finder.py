from math import radians, cos, sin, asin, sqrt
from battles.models import Battle


class BattleFinder:
    """
    User instantiates BattleFinder with their lat and long as init arguments. This will then be used
    to find the nearest battles via the get_nearest_battles method.
    """

    def __init__(self, latitude, longitude):
        self.lat = float(latitude)
        self.long = float(longitude)

    def calculate_battle_distance(self, battle_lat, battle_long):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees) -- this utilizes the haversine formula
        """
        # convert decimal degrees to radians
        lat1, long1, lat2, long2 = map(radians, [self.lat, self.long, battle_lat, battle_long])

        # haversine formula
        longitude_difference = long2 - long1
        latitude_difference = lat2 - lat1
        a = sin(latitude_difference / 2) ** 2 + cos(lat1) * cos(lat2) * sin(longitude_difference / 2) ** 2
        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return km

    def convert_to_json_serializable(self, list_to_convert):
        """
        Database objects are convert to JSON serializable format so that they can be passed to the JavaScript template
        """
        json_serializable_list = []
        for item in list_to_convert:
            json_serializable_list.append({
                'name': item.name,
                'latitude': item.latitude,
                'longitude': item.longitude,
                'url': item.wiki_link,
                'date': item.date,
            })
        json_serializable_list = self.spread_if_too_close_together(json_serializable_list)
        return json_serializable_list

    def spread_if_too_close_together(self, json_list):
        """
        This method checks to see if there are any duplicate coordinates inside the list of ten battles,
        and if there are, offsets one of the duplicates by 0.001%.
        """
        dup_lats_counter = 1
        dup_longs_counter = 1
        for new_item in range(len(json_list)):
            for other_item in range(len(json_list)):
                if new_item == other_item:
                    continue
                else:
                    if json_list[new_item]['latitude'] == json_list[other_item]['latitude']:
                        lat_to_alter = float(json_list[new_item]['latitude'])
                        for n in range(dup_lats_counter):
                            lat_to_alter += lat_to_alter * 0.00001
                        json_list[new_item]['latitude'] = str(lat_to_alter)
                        dup_lats_counter += 1
                    if json_list[new_item]['longitude'] == json_list[other_item]['longitude']:
                        long_to_alter = float(json_list[new_item]['longitude'])
                        for n in range(dup_longs_counter):
                            long_to_alter += long_to_alter * 0.00001
                        json_list[new_item]['longitude'] = str(long_to_alter)
                        dup_longs_counter += 1
        return json_list

    def get_nearest_battles(self, list_start, list_end):
        """The list start and list end parameters allow for the user to request ten more battles."""
        all_battles = Battle.objects.all()
        sorted_list = sorted(all_battles, key=lambda battle: self.calculate_battle_distance(
            float(battle.latitude),
            float(battle.longitude)
        ))
        nearest_battles = self.convert_to_json_serializable(sorted_list[list_start:list_end])
        return nearest_battles
