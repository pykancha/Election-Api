import json
import time

from flask import Flask, render_template, request

from scraper import kantipur_election

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/area")
def area():
    name = request.args.get("name")
    url = f"https://election.ekantipur.com/{name}?lng=eng"
    data = kantipur_election(url)
    return json.dumps(data)


@app.route("/url/")
def url():
    url = request.args.get("url")
    print("Got url", url)
    data = kantipur_election(url)
    return json.dumps(data)


@app.route("/bulk")
def bulk():
    list_ = request.args.get("list")
    areas = list_.split(",")
    all_data = {}
    for area in areas:
        url = f"https://election.ekantipur.com/{area}?lng=eng"
        print("Requesting", url)
        data = kantipur_election(url)
        _, district = parse_area(area)
        all_data[district] = data
        time.sleep(1)
    return json.dumps(all_data)


def parse_area(area):
    area_parts = area.split("-")
    print(":: Area parsing", area_parts)
    state_no, district = area_parts[1], area_parts[-1]
    return state_no, district


@app.route("/summary")
def summary():
    temp = {}
    return json.dumps(temp)


if __name__ == "__main__":
    app.run(port=8090)
