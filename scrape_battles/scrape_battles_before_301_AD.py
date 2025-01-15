# All battle data scraped using BeautifulSoup via each page
# listed on https://en.wikipedia.org/wiki/Category:Lists_of_battles_by_date

# The only manual data entry required for the data set
# on this page was removing a bit of extra whitespace between dates

from bs4 import BeautifulSoup
import requests
import csv

response = requests.get('https://en.wikipedia.org/wiki/List_of_battles_before_301')
data = response.content
soup = BeautifulSoup(data, 'html.parser')

with open('battles.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    list_of_rows = soup.find_all('tr')
    list_of_dates = []
    for row in list_of_rows:
        target_row = row.find_all('td')
        if target_row:
            try:
                date_column = target_row[-3]
                battle_date = date_column.get_text().strip()
                if "BC" not in battle_date:
                    battle_date = f"{battle_date} AD"
                print(battle_date)
                list_of_dates.append(battle_date)
            except AttributeError:
                date_link = date_column.find('a')
                battle_date = date_link.get_text().strip()
                if "BC" not in battle_date:
                    battle_date = f"{battle_date} AD"
                print(battle_date)
                list_of_dates.append(battle_date)
            except IndexError:
                battle_date = list_of_dates[-1]
            battle_link = target_row[-2].find('a')
            link_title = battle_link.attrs['title']
            if "(page does not exist)" in link_title:
                continue
            else:
                href = battle_link.attrs['href']
                battle_url = f"https://en.wikipedia.org{href}"
                battle_name = battle_link.get_text()
                writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})


fieldnames = ['name', 'url', 'date']
writer = csv.DictWriter(file, fieldnames=fieldnames)
list_of_rows = soup.find_all('tr')
list_of_dates = []
for row in list_of_rows:
    target_row = row.find_all('td')
    if target_row:
        try:
            date_column = target_row[-3]
            battle_date = date_column.get_text().strip()
            if "BC" not in battle_date:
                battle_date = f"{battle_date} AD"
            print(battle_date)
            list_of_dates.append(battle_date)
        except AttributeError:
            date_link = date_column.find('a')
            battle_date = date_link.get_text().strip()
            if "BC" not in battle_date:
                battle_date = f"{battle_date} AD"
            print(battle_date)
            list_of_dates.append(battle_date)
        except IndexError:
            battle_date = list_of_dates[-1]
        battle_link = target_row[-2].find('a')
        link_title = battle_link.attrs['title']
        if "(page does not exist)" in link_title:
            continue
        else:
            href = battle_link.attrs['href']
            battle_url = f"https://en.wikipedia.org{href}"
            battle_name = battle_link.get_text()
            # writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})
