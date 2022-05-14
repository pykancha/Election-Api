"""
Script to scrape news from www.kantipurdaily.com/news
Contains:
    kantipur_daily_extractor(): Gives list of news dicts
"""
import json
from bs4 import BeautifulSoup as BS
import requests
from datetime import datetime

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
    news_list = []
    from pprint import pprint
    for article in soup.find_all("div", class_="candidate-meta-wrapper"):
         name = article.find('div', class_='candidate-name').text
         party = article.find('div', class_='candidate-party-name').text
         vote_no = article.find('div', class_='vote-numbers').text
         data_dict = {
            "candidate-name": name,
            "candidate-party-name": party,
            "vote-numbers": vote_no,
         }
         news_list.append(data_dict)
         counter += 1
    pprint(news_list)
    return news_list


def format_date(raw_date):
    org_format = "%Y/%m/%d"
    datetime_obj = datetime.strptime(raw_date, org_format)
    dest_format = "%d %b %Y"
    date = datetime_obj.strftime(dest_format)
    return date


if __name__ == "__main__":
    with open('data.json', 'r') as rf:
        data = json.load(rf)
        cities = data.keys()
    kantipur_election(data['kathmandu'])
