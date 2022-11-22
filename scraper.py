"""
Script to scrape news from www.kantipurdaily.com/news
Contains:
    kantipur_daily_extractor(): Gives list of news dicts
"""
import json
from datetime import datetime

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
    from pprint import pprint

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
    for candidate_info in article.find_all("div", class_="candidate-wrapper"):
        name = candidate_info.find("div", class_="nominee-name").text
        party = candidate_info.find("div", class_="candidate-party-name").text
        votes = candidate_info.find("div", class_="vote-count").text
        info_list.append(
            {
                "name": name.strip(),
                "party": party.strip(),
                "votes": votes.strip(),
            }
        )
    return info_list


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
