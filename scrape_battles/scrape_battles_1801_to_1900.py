# This page's HTML structure as it pertains to the desired information is as follows:

# From years 1801 to 1815:
# Page main body <div>
#   List of battles across a few years <ul>
#       List of battles and the year header (within one year) <li>
#           Year span <span>
#               Battle year text <span>
#           List of battles below year span <ul>
#               Battle list item <li>
#                   Battle link containing battle_url and battle_name <a>

# From years 1816 to 1900:
# Page main body <div>
#   List of battles across a few years <ul>
#       List of battles and ****the year text**** <-- this time, the year text is inside the li (within one year) <li>
#           List of battles below date span <ul>
#               Battle list item <li>
#                   Battle link containing battle_url and battle_name <a>

# Code commented out below was used to manually parse through the data to check for false battles on the page

from bs4 import BeautifulSoup
import requests
import csv

response = requests.get('https://en.wikipedia.org/wiki/List_of_battles_1801%E2%80%931900')
data = response.content
soup = BeautifulSoup(data, 'html.parser')
text_to_replace = ["-", "–", "\n"]

page_main_body_div = soup.select('.mw-parser-output')[0]
div_children = page_main_body_div.findChildren(recursive=False)

# list_of_battle_urls = []

with open('battles.csv', 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for element in range(6, 9):
        if div_children[element].name == "ul":
            target_lis = div_children[element].findChildren(recursive=False)
            for li in target_lis:
                li_children = li.findChildren(recursive=False)
                for child in li_children:
                    if child.name == "span":
                        battle_date = child.text
                        battle_date = battle_date.strip()
                    if child.name == "ul":
                        battle_child_lis = child.findChildren(recursive=False)
                        for battle_child in battle_child_lis:
                            link = battle_child.find('a')
                            battle_name = link.attrs["title"]
                            href = link.attrs["href"]
                            battle_url = f"https://en.wikipedia.org{href}"
                            writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})
                            # list_of_battle_urls.append(battle_url)

    for element in range(9, 24):
        if div_children[element].name == "ul":
            target_lis = div_children[element].findChildren(recursive=False)
            for li in target_lis:
                battle_date = li.find(text=True)
                for text_item in text_to_replace:
                    if text_item in battle_date:
                        battle_date = battle_date.replace(text_item, "").strip()
                target_li_children = li.findChildren(recursive=False)
                for child in target_li_children:
                    if child.name == "ul":
                        battle_child_lis = child.findChildren(recursive=False)
                        for battle_child in battle_child_lis:
                            try:
                                link = battle_child.find('a')
                                battle_name = link.attrs["title"]
                                href = link.attrs["href"]
                                if "(page does not exist)" in battle_name:
                                    continue
                                battle_url = f"https://en.wikipedia.org{href}"
                            except AttributeError:
                                continue
                            else:
                                writer.writerow({'name': battle_name, 'url': battle_url, 'date': battle_date})
                                # list_of_battle_urls.append(battle_url)

# The following battles were listed as a subset of the "Ulm Campaign" in 1805, and so were manually added (since there
# were only five of these battles):
# Battle of Wertingen , https://en.wikipedia.org/wiki/Battle_of_Wertingen , 1805
# Battle of Günzburg , https://en.wikipedia.org/wiki/Battle_of_G%C3%BCnzburg , 1805
# Battle of Haslach-Jungingen , https://en.wikipedia.org/wiki/Battle_of_Haslach-Jungingen , 1805
# Battle of Elchingen , https://en.wikipedia.org/wiki/Battle_of_Elchingen , 1805
# Battle of Ulm , https://en.wikipedia.org/wiki/Battle_of_Ulm , 1805





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
# ]

# for url in list_of_battle_urls:
#     if any(keyword in url.lower() for keyword in keywords_to_check_for_real_battle):
#         pass
#     else:
#         print(url)


# Below are the manual database changes that were made as a result of manual parsing using the keywords above:

# Remove:
# James Wilkinson , https://en.wikipedia.org/wiki/James_Wilkinson , 1813
# Ulm campaign , https://en.wikipedia.org/wiki/Ulm_campaign , 1805


# Replace:
# *Konstantinos Kanaris , https://en.wikipedia.org/wiki/Konstantinos_Kanaris , 1822*
# With:
# *Burning of the Ottoman flagship off Chios
# https://en.wikipedia.org/wiki/Burning_of_the_Ottoman_flagship_off_Chios
# 1822*


# Replace:
# *First Assault on Morris Island , https://en.wikipedia.org/wiki/Fort_Wagner , 1863*
# With:
# *First Battle of Fort Wagner , https://en.wikipedia.org/wiki/First_Battle_of_Fort_Wagner , 1863*
