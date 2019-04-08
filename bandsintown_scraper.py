#Import the necessary methods from tweepy library

print 'BandsinTown Scraper 1.0'

from bs4 import BeautifulSoup
import requests
import json
import re # regular expression, I just use it to extract the JSON from the JavaScript

page = 'https://www.bandsintown.com/?came_from=257&page='
urlBucket = []
for i in range (0,3):
    uniqueUrl = page + str(i)
    urlBucket.append(uniqueUrl)

print urlBucket

for url in urlBucket:
    x = requests.get(url)

    soup = BeautifulSoup(x.content, 'html.parser')

    json_text = soup.find_all('script')[2].text  # Gives you a JSON set to the valirable window.__data
    json_extracted = re.search(r'^window.__data=(.+)', json_text).group(
        1)  # Collect the JSON without variable assigning
    json_parsed = json.loads(json_extracted)

    # The dates are being hidden in json.homeView.body.popularEvents.events
    for item in json_parsed['homeView']['body']['popularEvents']['events']:
        print(item['artistName'])
        print('Playing on', item['dayOfWeek'], item['dayOfMonth'], item['month'], '\n')


