# This page's HTML structure as it pertains to the desired information is as follows:

# Page main body <div>
#   h3 containing year <h3>
#       Year text <span>
#   table containing all battles for year above <table>
#       <tbody>
#           row containing battle info <tr>
#               <td>
#                   battle name and link <a>
#               **battle date (month and day) text**<td>

# Code commented out below was used to manually parse through the data to check for false battles on the page

from bs4 import BeautifulSoup
import requests
import csv

response = requests.get('https://en.wikipedia.org/wiki/List_of_battles_in_the_21st_century')
data = response.content
soup = BeautifulSoup(data, 'html.parser')
text_to_replace = ["-", "–", "\n"]

page_main_body_div = soup.select('.mw-parser-output')[0]
main_tags = page_main_body_div.findChildren(recursive=False)
relevant_tags = main_tags[4:48]

list_of_years = []
# list_of_battle_urls = []

with open('battles.csv', 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for tag in relevant_tags:
        if tag.name == "h3" or tag.name == "h2":
            year_spans = tag.findChildren(recursive=False)
            relevant_span = year_spans[0]
            year_text = relevant_span.text.strip()
            list_of_years.append(year_text)
        elif tag.name == "table":
            tbody = tag.find("tbody", recursive=False)
            all_table_rows = tbody.findChildren(recursive=False)
            for tr in all_table_rows:
                all_table_data_in_row = tr.findChildren(recursive=False)
                battle_name_td = all_table_data_in_row[0]
                date_td = all_table_data_in_row[1]
                try:
                    link = battle_name_td.find('a')
                    battle_name = link.attrs['title']
                except AttributeError:
                    continue
                else:
                    href = link.attrs["href"]
                    if "(page does not exist)" in battle_name:
                        continue
                    battle_url = f"https://en.wikipedia.org{href}"
                    battle_month_and_day = date_td.text.strip()
                    battle_year = list_of_years[-1]
                    if battle_year in battle_month_and_day:
                        battle_date = battle_month_and_day
                    else:
                        battle_date = f"{battle_month_and_day}, {battle_year}"
                    if " " in battle_date:
                        battle_date = battle_date.replace(" ", " ")
                    writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})
                    # list_of_battle_urls.append(battle_url)


# keywords_to_check_for_real_battle = [
#     "battle",
#     "siege",
#     "invasion",
#     "campaign",
#     "raid",
#     "massacre",
#     "bombardment",
#     "expedition",
#     "capture",
#     "rebellion",
#     "revolt",
#     "operation",
#     "attack",
#     "offensive",
#     "landing",
#     "action",
# ]

# for url in list_of_battle_urls:
#     if any(keyword in url.lower() for keyword in keywords_to_check_for_real_battle):
#         pass
#     else:
#         print(url)


# Below are the manual database changes that were made as a result of manual parsing using the keywords above:

# Replace:
# 2003 Invasion of Iraq , https://en.wikipedia.org/wiki/2003_Invasion_of_Iraq#Opening_attack , "26 March – 3 April, 2003"
# 2003 Invasion of Iraq , https://en.wikipedia.org/wiki/2003_Invasion_of_Iraq#Opening_attack , "27 & 28 March, 2003"
# 2003 invasion of Baghdad , https://en.wikipedia.org/wiki/2003_invasion_of_Baghdad , "3–12 April, 2003"
# 2003 Invasion of Iraq , https://en.wikipedia.org/wiki/2003_Invasion_of_Iraq#Opening_attack , "6 April, 2003"

# With:
# Battle of Najaf , https://en.wikipedia.org/wiki/Battle_of_Najaf_(2003) , 24 March – 4 April 2003
# Battle of Karbala , https://en.wikipedia.org/wiki/Battle_of_Karbala_(2003) , 23 March – 6 April 2003
# Battle of Baghdad , https://en.wikipedia.org/wiki/Battle_of_Baghdad_(2003) , April 3–9, 2003
# Battle of Basra , https://en.wikipedia.org/wiki/Battle_of_Basra_(2003) , 21 March – 6 April 2003


# Replace:
# Iraqi insurgency (Iraq War) , https://en.wikipedia.org/wiki/Iraqi_insurgency_(Iraq_War)#Moqtada_al-Sadr , "5 April – August, 2004"

# With:
# Battle of Najaf , https://en.wikipedia.org/wiki/Battle_of_Najaf_(2004) , 5–27 August 2004
