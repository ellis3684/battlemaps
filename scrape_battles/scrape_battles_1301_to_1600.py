# The Wikipedia table layout for this page got a bit funky from dates 1464-1465. Since this only affected
# three battles in total, I just ran the code as is and manually input the data for those three battles.

from bs4 import BeautifulSoup
import requests
import csv

response = requests.get('https://en.wikipedia.org/wiki/List_of_battles_1301%E2%80%931600')
data = response.content
soup = BeautifulSoup(data, 'html.parser')

with open('battles.csv', 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    list_of_rows = soup.find_all('tr')
    list_of_dates = []
    for row in list_of_rows[5:]:
        target_row = row.find_all('td')
        if target_row:
            try:
                date_column = target_row[-4]
                battle_date = date_column.get_text().strip()
                battle_date = f"{battle_date} AD"
                list_of_dates.append(battle_date)
            except AttributeError:
                date_link = date_column.find('a')
                battle_date = date_link.get_text().strip()
                battle_date = f"{battle_date} AD"
                list_of_dates.append(battle_date)
            except IndexError:
                battle_date = list_of_dates[-1]
            try:
                battle_link = target_row[-3].find('a')
                link_title = battle_link.attrs['title']
            except AttributeError:
                battle_name = target_row[-3].get_text().strip()
                print(battle_name)
                continue
            else:
                if "(page does not exist)" in link_title:
                    continue
                else:
                    href = battle_link.attrs['href']
                    battle_url = f"https://en.wikipedia.org{href}"
                    battle_name = battle_link.get_text()
                    writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})
