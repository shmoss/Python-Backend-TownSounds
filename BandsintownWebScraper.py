#Dependencies

print 'Let bandsintown scraping commence!'

from bs4 import BeautifulSoup
import requests
import string
import json
import geocoder
import mapbox
import selenium
from selenium import webdriver

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import datetime
from datetime import datetime as dt
import re
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

#Set driver options
options = Options()
options.add_argument('--no-sandbox') # Bypass OS security model
driverLocation = webdriver.Chrome(chrome_options=options, executable_path=r'/Applications/chromedriver 4')
driverLocation.quit()

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

# Set date one week from now
nowDate = datetime.datetime.now()
week = datetime.timedelta(weeks = 1)
oneWeek = custom_strftime('%A, %B {S}, %Y', dt.now() + week)
oneWeekSplit = oneWeek.split(',')
oneWeekDay = oneWeekSplit[1]
oneWeekDayCleaned = (re.sub(r'\D+$', '', oneWeekDay))
oneWeekDayFinal = (oneWeekSplit[0] + "," + oneWeekDayCleaned + "," + oneWeekSplit[2])
#p=datetime.datetime.strptime('June 5, 2019', '%b %d, %Y')
#print p
oneWeekDateTime = datetime.datetime.strptime(oneWeekDayFinal, '%A, %B %d, %Y')


# For testing, set date one day from now
day = datetime.timedelta(days=1)
oneDay = custom_strftime('%A, %B {S}, %Y', dt.now() + day)
oneDaySplit = oneDay.split(',')
oneDayfromNow = oneDaySplit[1]
oneDayCleaned = (re.sub(r'\D+$', '', oneDayfromNow))
oneDayFinal = (oneDaySplit[0] + "," + oneDayCleaned + "," + oneDaySplit[2])
oneDayDateTime = datetime.datetime.strptime(oneDayFinal, '%A, %B %d, %Y')
#print oneDayDateTime, oneWeekDateTime


#Set up geocoder
geocoder = mapbox.Geocoder(access_token='pk.eyJ1Ijoic3RhcnJtb3NzMSIsImEiOiJjam13ZHlxbXgwdncwM3FvMnJjeGVubjI5In0.-ridMV6bkkyNhbPfMJhVzw')

#Set up web driver and base URL
driver= webdriver.Chrome(executable_path='/Applications/chromedriver 4')

#Set base url
base_url = 'https://www.bandsintown.com/?came_from=257&page='

events = []
eventContainerBucket = []

for i in range(2,80):

    #cycle through pages in range
    driver.get(base_url + str(i))
    pageURL = base_url + str(i)

    # get events links
    event_list = driver.find_elements_by_css_selector('div[class^=eventList-] a[class^=event-]')
    # collect href attribute of events in even_list
    events.extend(list(event.get_attribute("href") for event in event_list))

print "total events: ", (len(events))

# iterate through all events and open them.
item = {}
allEvents = []
for event in events:

    driver.get(event)
    currentUrl = driver.current_url
    currentRequest = requests.get(currentUrl)
    #print currentRequest.status_code

    if currentRequest.status_code == 200:
        #print ("link working")

        try:
            driver.find_element_by_css_selector('[class^=eventInfoContainer-]')
            print "element exists!"
        except (ElementNotVisibleException, NoSuchElementException):
            print "element doesn't exist"
            continue



        soup = bs(driver.find_element_by_css_selector('[class^=eventInfoContainer-]').get_attribute('outerHTML'))
        soup2 = bs(driver.find_element_by_css_selector('[class^=artistAndEventInfo-]').get_attribute('outerHTML'))
        containers = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')
        date_time = containers[1].text.split('\n')

        # Only pull one weeks worth of data
        # Find date of event and format to compare against one week from now date
        dateMatch = soup.select_one('img + div').text
        dateMatchSplit = dateMatch.split(',')
        dateMatchDay = dateMatchSplit[1]
        dateMatchCleaned = (re.sub(r'\D+$', '', dateMatchDay))
        dateMatchDayFinal = (
                dateMatchSplit[0] + "," + dateMatchCleaned + "," + dateMatchSplit[2])
        dateMatchDate = datetime.datetime.strptime(dateMatchDayFinal, '%A, %B %d, %Y')
        eventDate = str(dateMatchDate).replace("00:00:00","")
        eventDate = eventDate.rstrip()

        #print dateMatchDate, oneWeekDateTime

        #compare date of event to one week from now date
        if dateMatchDate <= oneWeekDateTime:
            #print "this event occurs one week or less from today"

            # Get artist
            artist = soup2.select_one('h1').text


            # Get date
            date = soup.select_one('img + div').text
            dateSplit = date.split(',')
            dateSplitDay = dateSplit[1]
            dateSplitDayCleaned = (re.sub(r'\D+$', '', dateSplitDay))

            dSplit = dateSplitDayCleaned.split()
            month = dSplit[0]
            number = dSplit[1]

            dateFormatted = (dateSplit[0][0:3] + " " + month[0:3] + " " + number + dateSplit[2])
            print(artist, dateFormatted)

            # Get time
            time = soup.select_one('img + div + div').text

            # Get address
            address = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div + div').text

            # Get venue
            venue = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div').text

            #Get image
            artistImage = soup.select_one('img')
            artistImage=driver.find_element_by_xpath("//div[@class='artistAndEventInfo-7c13900b']//img").get_attribute("src")

            #Get genre information
            genre = 'No genre available'
            try:
                genre = driver.find_element_by_xpath("//div[@class='artistBio-833c365c']").text
            except (ElementNotVisibleException, NoSuchElementException):
                pass

            #Get other information
            otherInfo = "No other event info available"
            try:
                otherInfo = driver.find_element_by_xpath("//div[@class='eventInfoContainer-a1c6de30']").text
            except (ElementNotVisibleException, NoSuchElementException):
                pass



            # Get artist bio
            artistBio = "No artist bio available"
            try:
                artistBio = driver.find_element_by_xpath("//div[@class='artistBio-cdbd5bde']").text
            except (ElementNotVisibleException, NoSuchElementException):
                pass

            # Capture additional bio info
            readMore = 'artistBio-322df114'
            try:
                driver.find_element_by_xpath("//div[@class='artistBio-322df114']").click();
                #print(moreInfo)
            except (ElementNotVisibleException, NoSuchElementException):
                pass

            #Regardless of whether or not there is "Read More", print complete bio info.
            moreBioInfo = "No artist bio available"
            try:
                moreBioInfo = driver.find_element_by_xpath("//div[@class='artistBio-cdbd5bde']").text
                print("more bio info is:", moreBioInfo)
            except (ElementNotVisibleException, NoSuchElementException):
                print('no moreBioInfo')
                pass



            #print artistBio, otherInfo, genre

            #Geocode address
            geocodeInput = venue + ", " + address
            response = geocoder.forward(address)
            result = response.json()

            #Bin information into 'item'
            item['Artist'] = artist
            item['Date'] = dateFormatted
            item['eventDate'] = eventDate
            item['Time'] = time
            item['Venue'] = venue
            item['Address'] = address
            item['artistImage'] = artistImage
            item['genre'] = genre
            item['otherInfo'] = otherInfo
            item['moreBioInfo'] = moreBioInfo
            #print(moreBioInfo)

            # Get latitude, longitude
            coordinates = result['features'][0]['center']
            item['Coordinates'] = coordinates

            # Format output to JSON
            case = {'Artist': item['Artist'], 'Date': item['Date'], 'EventDate': item['eventDate'], 'Time': item['Time'], 'Venue': item['Venue'],
            'Address': item['Address'], 'Coordinates': coordinates, 'ArtistImage': item['artistImage'], 'Genre': item['genre'], 'otherInfo': item['otherInfo'], 'moreBioInfo': item['moreBioInfo']}

            item[event] = case

            #print case
            allEvents.append(case)


        elif currentRequest.status_code != 200:  # could also check == requests.codes.ok
            continue

#eventsVariable = "var SFEvents = "
#print item
#print allEvents
#allEvents = eventsVariable + allEvents

#with open("testScrape.json", "w") as writeJSON:
   #file_str = json.dumps(allEvents, sort_keys=True)
   #file_str = "var events = " + file_str
   #writeJSON.write(file_str)

with open("/Users/starrmoss/Documents/TownSounds_Javascript/data/sf_events_2.json", "w") as writeJSON:
    file_str = json.dumps(allEvents, sort_keys=True)
    file_str = "var sf_events_3 = " + file_str
    writeJSON.write(file_str)

print "Data pull complete!"