# This page's HTML structure as it pertains to the desired information is as follows:

# Page main body <div>
#   List of years/battles across a period of years <ul>
#       List of particular year's battles **Text contains year** <li>
#           List of all battles in that year (excluding the year text) <ul>
#               List item for one battle <li>
#                   Battle name and link <a>

# Code commented out below was used to manually parse through the data to check for false battles on the page

from bs4 import BeautifulSoup
import requests
import csv

response = requests.get('https://en.wikipedia.org/wiki/List_of_battles_1901%E2%80%932000')
data = response.content
soup = BeautifulSoup(data, 'html.parser')
text_to_replace = ["-", "–", "\n"]

page_main_body_div = soup.select('.mw-parser-output')[0]
div_children = page_main_body_div.findChildren(recursive=False)

# list_of_battle_urls = []

with open('battles.csv', 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for element in range(7, 20):
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


# The following code was used to extract battles that were contained as a subset <ul> within a target <li> element.
# Wikipedia likely formatted these battles in this manner to show the battles as a subset of a particular war,
# since the original target <li> contained the name of the entire war/campaign.

# Ex: The target <li> displayed Yom Kippur War, and the <ul> within the target <li> showed all battles that
# occurred as part of the Yom Kippur War.

# These values were extracted to a separate csv file then copy and pasted into the main battles.csv file
# (since there were only 33 of these battles).


with open('oddly_formatted_battles.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['name', 'url', 'date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for element in range(7, 20):
        if div_children[element].name == "ul":
            target_lis = div_children[element].findChildren(recursive=False)
            for mother_li in target_lis:
                battles_in_specific_campaign_ul = mother_li.findChildren(recursive=False)
                for subset in battles_in_specific_campaign_ul:
                    if subset.name == "ul":
                        new_target_lis = subset.findChildren(recursive=False)
                        for li in new_target_lis:
                            try:
                                battle_date = li.find(text=True)
                                for text_item in text_to_replace:
                                    if text_item in battle_date:
                                        battle_date = battle_date.replace(text_item, "").strip()
                            except TypeError:
                                continue
                            else:
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
                                                writer.writerow(
                                                    {
                                                        'name': battle_name,
                                                        'url': battle_url,
                                                        'date': battle_date
                                                    }
                                                )


# I also manually extracted the following four battles since they were formatted as part of the <li> text containing
# the text for a year:
# Bay of Pigs Invasion , https://en.wikipedia.org/wiki/Bay_of_Pigs_Invasion , 1961
# Battle of Dien Bien Phu , https://en.wikipedia.org/wiki/Battle_of_Dien_Bien_Phu , 1954
# Battle of Vĩnh Yên , https://en.wikipedia.org/wiki/Battle_of_V%C4%A9nh_Y%C3%AAn , 1951
# Battle of Uijeongbu (1951) , https://en.wikipedia.org/wiki/Battle_of_Uijeongbu_(1951) , 1951


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

# Remove:
# Telavåg , https://en.wikipedia.org/wiki/Telav%C3%A5g , 1942
# Indo-Pakistani War of 1947 , https://en.wikipedia.org/wiki/Indo-Pakistani_War_of_1947 , 1947
# 1948 Arab–Israeli War , https://en.wikipedia.org/wiki/1948_Arab%E2%80%93Israeli_War , 1948
# Sino-Indian War , https://en.wikipedia.org/wiki/Sino-Indian_War , 1962
# Second Kashmir War , https://en.wikipedia.org/wiki/Second_Kashmir_War , 1965
# Six-Day War , https://en.wikipedia.org/wiki/Six-Day_War , 1967
# USS Pueblo (AGER-2) , https://en.wikipedia.org/wiki/USS_Pueblo_(AGER-2) , 1968
# Football War , https://en.wikipedia.org/wiki/Football_War , 1969
# Indo-Pakistani War of 1971 , https://en.wikipedia.org/wiki/Indo-Pakistani_War_of_1971 , 1971
# Yom Kippur War , https://en.wikipedia.org/wiki/Yom_Kippur_War , 1973
# Ogaden War , https://en.wikipedia.org/wiki/Ogaden_War , 1977
# Iran–Iraq War , https://en.wikipedia.org/wiki/Iran%E2%80%93Iraq_War , 1980
# 1982 Lebanon War , https://en.wikipedia.org/wiki/1982_Lebanon_War , 1982
# Falklands War , https://en.wikipedia.org/wiki/Falklands_War , 1982
# Gulf War , https://en.wikipedia.org/wiki/Gulf_War , 1990
# Gulf War , https://en.wikipedia.org/wiki/Gulf_War , 1991
# Afghanistan , https://en.wikipedia.org/wiki/Afghanistan , 1994
# Kargil War , https://en.wikipedia.org/wiki/Kargil_War , 1999


# Replace:
# Triest , https://en.wikipedia.org/wiki/Triest#Yugoslav_and_New_Zealand_involvement , 1945
# With:
# Trieste operation , https://en.wikipedia.org/wiki/Trieste_operation , 1945


# Lastly, battles scraped for the year 1951 required manual data manipulation to correct the year shown
# since the HTML tags for that portion of the page were different than the rest.
