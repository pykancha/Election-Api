# Nepal Election API 2079

Developed using the fantastic beautifulsoup scraping library, data source is [ekantipur](https://election.ekantipur.com)

This repo was developed as backend for election-bot for reddit hosted at https://github.com/pykancha/reddit-bots

Hosted at https://flaskapi.osac.org.np

## Installation
- Install python
- Clone the repo
```
git clone https://github.com/pykancha/election-api
cd election-api
```
- Install dependencies
```
poetry install # or pip install -r requirements.txt
```
- Run the server
```
poetry run python main.py # or python main.py
```

## Usage
###### AreaName

Requests at

```
/area?name=pradesh-1/district-jhapa
```

where name is valid kantipur url part representing an electoral area.
This is supposed to be extracted from a kantipur url.

Example: https://flaskapi.osac.org.np/area?name=pradesh-1/district-jhapa

###### URL

Requests at

```
/url?url=https://election.ekantipur.com/pradesh-1/district-jhapa?lng=eng
```

where url must be valid kantipur url in format similar to url in above example.

Example: https://flaskapi.osac.org.np/url?url=https://election.ekantipur.com/pradesh-1/district-jhapa?lng=eng

###### Bulk List
Requests at

```
/bulk?list=pradesh-1/district-jhapa,pradesh-3/district-kathmandu
```

Where list must be list of valid AreaNames sepearated by commas.

Example: https://flaskapi.osac.org.np/bulk?list=pradesh-1/district-jhapa,pradesh-3/district-kathmandu


###### Summary

Requests at

```
/summary
```

Gives all party names, their wins and leads count in Federal and provincial category.

Example: https://flaskapi.osac.org.np/summary
