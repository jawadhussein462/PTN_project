url = "https://www.myfrenchstartup.com/ajax/advancedsearch.php"

import requests

headers = {
    "authority": "www.myfrenchstartup.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "accept": "*/*",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.myfrenchstartup.com",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.myfrenchstartup.com/fr/recherche-avancee",
    "accept-language": "fr-FR,fr;q=0.9,en;q=0.8,en-US;q=0.7",
    "cookie": "PHPSESSID=1214a6472ce75d0cf048a69c92ec565c",
}

from bs4 import BeautifulSoup
import csv

csv_file = open("myfrenchstartup.csv", 'w', newline='', encoding="utf-8")
wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

startups = []

for page in range(1, 1500):

    payload = {"keyword_search": "",
               "startup_name": "",
               "list_sector": "",
               "list_sous_sector": "",
               "list_marche": "",
               "list_sous_marche": "",
               "region": "",
               "date_deb": "",
               "date_fin": "",
               "effectif": "",
               "naf": "",
               "raised_funds_A": "",
               "raised_funds_B": "",
               "raised_funds_C": "",
               "raised_funds_D": "",
               "raised_funds_E": "",
               "raised_funds_F": "",
               "recrurement": "",
               "date_lf": "",
               "montant_lf": "",
               "difficulte": "",
               "page": str(page)}

    response = requests.post(url, payload, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content)
        soup_startups = soup.find_all("li", {"class": "media"})

        for startup in soup_startups:
            name = startup.find("h6", {"class": "media-heading"}).find("a").text
            categories = [x.strip() for x in startup.find("div", {
                "style": "font-style: italic; font-size: 12px; color: #999; padding-bottom: 5px;"}).text.split("-")]
            subcategories = []

            for category in categories:
                subcategory = [x.strip() for x in category.split("/")]
                subcategories += subcategory

            labels = [label.text.strip() for label in startup.find_all("span", {"class": "token-label"})]
            description = startup.find("p").text.strip()

            wr.writerow([name, subcategories + labels, description])
            startups.append((name, subcategories + labels, description))

        print("page: ", page, "startup:", startups[-1])
    else:
        print("page: ", page, "error: ", response.status_code)

# import pandas as pd

# for startup in startups:
#     print(startup[0])
