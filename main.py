import json
from flask import Flask, request, render_template
from scraper import kantipur_election

app = Flask(__name__)  # notice that the app instance is called `app`, this is very important.
with open('data.json', 'r') as rf:
    data = json.load(rf)
    cities = data.keys()

@app.route("/")
def home():
   return render_template('README.html')

@app.route("/<city>")
def main(city):
    if city not in cities:
        return f"404, No city named '{city}'"
    print("GOT city", city)
    return json.dumps(kantipur_election(data[city]))

@app.route("/url/")
def other():
    url = request.args.get('url')
    print("Got url", url)
    if not url:
       return "Please, send 'url' as request argument"
    return json.dumps(kantipur_election(url))
