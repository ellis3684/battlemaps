import csv
import requests
from bs4 import BeautifulSoup


# All battle pages that show coordinates seem to have span element that has {class: geo-dec}
# and text is the coords labeled as such "53.153°N 10.835°E"
# Battle num 6954 has one set of coords on page - Battle of Konna


# Some are different - and have lat and long listed as such:
# one span element of {class: latitude} with text = "44°11′56.44″N"
# and one span element of {class: longitude} with text = "12°24′5.62″E"

# So far, all have parent or grandparent span element of {class: geo-default}

# All appear to fit on of the above two rules, and so we'll use these classes to target our coordinate data.

# Battle num 6248 - Battle of Borodino has a wiki link that links to a
# subsection of the page - try and see if can still scrape data needed from it

with open('battles.csv', 'r', newline='', encoding='utf-8') as file:
    complete_list_of_battles = list(csv.DictReader(file))


with open('battles_with_coords.csv', 'w', newline='', encoding='utf-8') as new_file:
    fieldnames = ['battle', 'link', 'date', 'coordinates']
    writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    writer.writeheader()
    for battle in complete_list_of_battles:
        target_url = battle['link']
        response = requests.get(target_url)
        print(response.raise_for_status())
        data = response.content
        soup = BeautifulSoup(data, 'html.parser')
        has_coordinates = soup.find('span', class_='geo-dec')
        if has_coordinates is None:
            continue
        coordinates = has_coordinates.text
        battle_name = battle['battle']
        battle_url = battle['link']
        battle_date = battle['date']
        writer.writerow({'battle': battle_name, 'link': battle_url, 'date': battle_date, 'coordinates': coordinates})
