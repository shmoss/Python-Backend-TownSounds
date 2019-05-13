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
import datetime


from datetime import datetime as dt

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

nowDate = datetime.datetime.now()
oneWeeks = datetime.timedelta(weeks = 1)
week = nowDate + oneWeeks

oneWeekFromNow = custom_strftime('%A, %B {S}, %Y', dt.now() + oneWeeks)
print "oneWeekFromNow is: " + oneWeekFromNow

#oneWeekFromToday = todaysDate + oneWeek

#print "oneWeekFromToday is: " + oneWeekFromToday

now = datetime.datetime.now()
print (now.strftime("%A, %b %d, %Y"))


oneWeek = datetime.timedelta(weeks = 1)

weekFromToday = now + oneWeek
print (weekFromToday.strftime("%A, %b %d, %Y"))
weekFromTodayString = custom_strftime('%A, %B {S}, %Y', dt.now())

testVariable = "Monday, May 13th, 2019"

#Set up geocoder
geocoder = mapbox.Geocoder(access_token='pk.eyJ1Ijoic3RhcnJtb3NzMSIsImEiOiJjam13ZHlxbXgwdncwM3FvMnJjeGVubjI5In0.-ridMV6bkkyNhbPfMJhVzw')


#Set up web driver and base URL
driver= webdriver.Chrome(executable_path='/Applications/chromedriver74')

base_url = 'https://www.bandsintown.com/?came_from=257&page='
#this page gives 404 error!
#https://www.bandsintown.com/e/1009883476-kronos-quartet-and-mahsa-vahdat-at-weill-hall?came_from=257&utm_medium=web&utm_source=home&utm_campaign=event
events = []
eventContainerBucket = []
for i in range(1, 40):
    #pageSource = driver.page_source
    #print pageSource + "page source"
    #if not driver.page_source().contains("404"):
    #and
    #if not driver.getPageSource().contains("not found"):
    driver.get(base_url + str(i))
    pageURL = base_url + str(i)
    #print pageURL
    #r = requests.get(pageURL)
    #print(r.status_code)
    #r = requests.get(pageURL)
    #print (r.status_code)

    # get events links
    event_list = driver.find_elements_by_css_selector('div[class^=eventList-] a[class^=event-]')
    # collect href attribute of events in even_list
    events.extend(list(event.get_attribute("href") for event in event_list))

print(len(events))

# iterate throw all events and open them.
item = {}
for event in events:

    driver.get(event)
    currentUrl = driver.current_url
    currentRequest = requests.get(currentUrl)
    print currentRequest.status_code

    if currentRequest.status_code == 200:
        print ("link working")

        #print event
        #uniqueEventContainer = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')[0]
        soup = bs(driver.find_element_by_css_selector('[class^=eventInfoContainer-]').get_attribute('outerHTML'))
        soup2 = bs(driver.find_element_by_css_selector('[class^=artistAndEventInfo-]').get_attribute('outerHTML'))
        containers = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')
        date_time = containers[1].text.split('\n')

        dateMatch = soup.select_one('img + div').text
        if dateMatch <= oneWeekFromNow:
            print "match!"

            #print soup
            #print soup2
            artist = soup2.select_one('h1').text
            #print artist
            #print artist
            date = soup.select_one('img + div').text
            time = soup.select_one('img + div + div').text
            #thing = soup.select_one('img + div + div + img').text
            address = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div + div').text

            venue = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div').text
            geocodeInput = venue + ", " + address
            print geocodeInput

            #Geocode address
            response = geocoder.forward(address)
            result = response.json()

            #Bin into 'item'
            item['Artist'] = artist
            item['Date'] = date
            item['Time'] = time
            item['Venue'] = venue
            item['Address'] = address

            print ("date is:" + date)


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
            #print result['features'][1]['center']
            coordinates = result['features'][0]['center']
            item['Coordinates'] = coordinates

            print result
            print address, str(coordinates)
            #print "Geocode input, Coords are: " + address, coordinates
            #print ["%0.6f" % i for i in coordinates]
            #print item
            #for element in result['features']:
                #coordinates = element['center']
                #
                #print address, coordinates

            case = {'Artist': item['Artist'], 'Date': item['Date'], 'Time': item['Time'], 'Venue': item['Venue'],
            'Address': item['Address'], 'Coordinates': item['Coordinates']}
            item[event] = case

        print item

with open("testScrape.json", "w") as writeJSON:
   json.dump(item, writeJSON)
    #for uniqueDate = i.find_all('div', {'class': 'event-b58f7990'})
    #print (uniqueDate)


print result