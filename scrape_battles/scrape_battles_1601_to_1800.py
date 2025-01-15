# This page's HTML structure as it pertains to the desired information is as follows:
# Half century <ul>
#    Year <li>
#        Battles for that year <ul>
#            Battle <li>
#                Battle link <a>


# Manual parsing of data for this page involved checking battles whose hrefs did not contain battle-related keywords
# After doing so, the following manual changes were made:

# Remove below battles from csv
# L'Escalade , https://en.wikipedia.org/wiki/L%27Escalade , 1602 AD
# 1718 in piracy , https://en.wikipedia.org/wiki/1718_in_piracy , 1718 AD
# Patrona Halil , https://en.wikipedia.org/wiki/Patrona_Halil , 1730 AD
# HMS Hermione (1782) , https://en.wikipedia.org/wiki/HMS_Hermione_(1782) , 1797 AD

# Alter info for below battles accordingly
# From:
# Sinhagad , https://en.wikipedia.org/wiki/Sinhagad , 1670 AD
# To:
# Battle of Sinhagad , https://en.wikipedia.org/wiki/Battle_of_Sinhagad , 1670 AD

from bs4 import BeautifulSoup
import requests
import csv

response = requests.get('https://en.wikipedia.org/wiki/List_of_battles_1601%E2%80%931800')
data = response.content
soup = BeautifulSoup(data, 'html.parser')

all_lists_on_page = soup.select('.mw-parser-output > ul')
all_half_century_uls = all_lists_on_page[:4]

with open('battles.csv', 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for half_century_ul in all_half_century_uls:
        all_year_li_elements = half_century_ul.find_all('li', recursive=False)
        for single_year_li in all_year_li_elements:
            year_text = single_year_li.find(text=True, recursive=False)
            text_to_replace = ["-", "–", "\n"]
            for text_item in text_to_replace:
                if text_item in year_text:
                    year_text = year_text.replace(text_item, "").strip()
            battle_date = f"{year_text} AD"

            all_battle_li_elements = single_year_li.select('ul li')
            for battle_li in all_battle_li_elements:
                battle_a = battle_li.find('a')
                battle_name = battle_a.attrs['title']
                if "(page does not exist)" in battle_name:
                    continue
                href = battle_a.attrs['href']
                battle_url = f"https://en.wikipedia.org{href}"
                writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})


