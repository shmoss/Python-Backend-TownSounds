#Dependencies

print 'Let bandsintown scraping commence!'

from bs4 import BeautifulSoup
import requests
import json
import geocoder
import mapbox
import selenium
from selenium import webdriver

from selenium import webdriver
from bs4 import BeautifulSoup as bs

#Set up geocoder
geocoder = mapbox.Geocoder(access_token='pk.eyJ1Ijoic3RhcnJtb3NzMSIsImEiOiJjam13ZHlxbXgwdncwM3FvMnJjeGVubjI5In0.-ridMV6bkkyNhbPfMJhVzw')


#Set up web driver and base URL
driver= webdriver.Chrome(executable_path='/Applications/chromedriver')

base_url = 'https://www.bandsintown.com/?came_from=257&page='
events = []
eventContainerBucket = []
for i in range(1, 2):
    driver.get(base_url + str(i))

    # get events links
    event_list = driver.find_elements_by_css_selector('div[class^=eventList-] a[class^=event-]')
    # collect href attribute of events in even_list
    events.extend(list(event.get_attribute("href") for event in event_list))

print(len(events))

# iterate throw all events and open them.
item = {}
for event in events:

    driver.get(event)
    #print event
    #uniqueEventContainer = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')[0]
    soup = bs(driver.find_element_by_css_selector('[class^=eventInfoContainer-]').get_attribute('outerHTML'))
    soup2 = bs(driver.find_element_by_css_selector('[class^=artistAndEventInfo-]').get_attribute('outerHTML'))
    containers = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')
    date_time = containers[1].text.split('\n')
    print soup
    print soup2
    artist = soup2.select_one('h1').text
    print artist
    #print artist
    date = soup.select_one('img + div').text
    time = soup.select_one('img + div + div').text
    #thing = soup.select_one('img + div + div + img').text
    address = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div + div').text
    response = geocoder.forward(address)
    result = response.json()
    venue = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div').text

    #Bin into 'item'
    item['Artist'] = artist
    item['Date'] = date
    item['Time'] = time
    item['Venue'] = venue
    item['Address'] = address

    case = {'Artist': item['Artist'], 'Date':  item['Date'], 'Time': item['Time'], 'Venue': item['Venue'], 'Address': item['Address']}
    item[event] = case
    #print item

    # address = soup.select_one('[class^=eventInfoContainer-]:nth-of-type(3) div + div').text
    # print(date, time, address)
    #locationImg = soup.select_one('[src="https://assets.bandsintown.com/images/pin.svg"]')['src']
    #t = locationImg.find_next_sibling("div")
    #thing = driver.find_element_by_css_selector("img[src='https://assets.bandsintown.com/images/pin.svg']") #this works
    #venue_address = place.text.split('\n')
    #venue = venue_address[0]
    #address = venue_address[1]

    #print date, time, venue, address
    #item[event] = item
    print item

print item
with open("testScrape.json", "w") as writeJSON:
   json.dump(item, writeJSON, ensure_ascii=False)
    #for uniqueDate = i.find_all('div', {'class': 'event-b58f7990'})
    #print (uniqueDate)


print result