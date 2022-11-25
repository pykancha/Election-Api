import json
from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup as BS

parser = "lxml"


def setup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit\
        /537.36(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("Connection refused by the server..", e)
    soup = BS(page.content, parser)
    return soup


def kantipur_election(url):
    soup = setup(url)
    counter = 0
    results = dict()

    for article in soup.find_all("div", class_="col-md-6"):
        constituency_name = article.find("h3", class_="card-title").text
        constituency_name_parts = constituency_name.split(" ")
        constituency_name_parts = [
            i.strip().lower() for i in constituency_name_parts if i.strip() != ""
        ]
        constituency_no = int(constituency_name_parts[-1])
        if constituency_no <= counter:
            break
        else:
            counter = constituency_no
        results[f"constituency : {constituency_no}"] = fetch_nominee_data(article)
    return results


def fetch_nominee_data(article):
    info_list = []

    card_text = article.find("div", class_="win-lead-text").text
    has_won = "won with" in card_text
    for candidate_info in article.find_all("div", class_="candidate-wrapper"):
        name = candidate_info.find("div", class_="nominee-name").text
        party = candidate_info.find("div", class_="candidate-party-name").text
        votes = candidate_info.find("div", class_="vote-count").text
        info_list.append(
            {
                "name": name.strip(),
                "party": party.strip(),
                "votes": votes.strip(),
                "winner_declared": has_won,
            }
        )
    return info_list


def fetch_summary(url):
    soup = setup(url)
    results = dict()

    element = soup.find("div", class_="parties")
    for el in element.find_all("div", class_="col-md-6"):
        level_name = el.find("h2", class_="title").text.strip()
        level_name = level_name.split(" ")[0].strip().lower()
        level_data = []
        for e in el.find_all("div", class_="row--border"):
            party = e.find("div", class_="party-name").text.strip()
            nums = e.find_all("div", class_="number-display")
            wins = nums[0].text.strip()
            leads = nums[1].text.strip()
            level_data.append(dict(name=party, wins=wins, leads=leads))
        results[level_name] = level_data
    return results


def fetch_pr(url):
    soup = setup(url)
    results = []

    element = soup.find("div", class_="samanupatik-content")
    for el in element.find_all("div", class_="g-2"):
        party_name = el.find("a", class_="legend-pn").text.strip()
        votes = el.find_all("div", class_="col-auto")[-1].text.strip()
        print(party_name, votes)
        results.append(dict(name=party_name, votes=votes))

    return results


def format_date(raw_date):
    org_format = "%Y/%m/%d"
    datetime_obj = datetime.strptime(raw_date, org_format)
    dest_format = "%d %b %Y"
    date = datetime_obj.strftime(dest_format)
    return date


if __name__ == "__main__":
    with open("data.json", "r") as rf:
        data = json.load(rf)
        cities = data.keys()
    kantipur_election(data["kathmandu"])
