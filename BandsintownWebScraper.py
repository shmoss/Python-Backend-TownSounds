#Dependencies

print 'Let bandsintown scraping commence!'

from bs4 import BeautifulSoup
import requests
import string
import json
import geocoder
import geopy
from geopy.geocoders import Nominatim

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
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By

#Set driver options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1420,1080')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(chrome_options=options, executable_path=r'/Applications/chromedriver_91')


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
print(oneWeekDateTime)

# For testing, set date one day from now
day = datetime.timedelta(days=1)
oneDay = custom_strftime('%A, %B {S}, %Y', dt.now() + day)
oneDaySplit = oneDay.split(',')
oneDayfromNow = oneDaySplit[1]
oneDayCleaned = (re.sub(r'\D+$', '', oneDayfromNow))
oneDayFinal = (oneDaySplit[0] + "," + oneDayCleaned + "," + oneDaySplit[2])
oneDayDateTime = datetime.datetime.strptime(oneDayFinal, '%A, %B %d, %Y')
print oneDayDateTime, oneWeekDateTime


#Set up geocoder
#geocoder = mapbox.Geocoder(access_token='pk.eyJ1Ijoic3RhcnJtb3NzMSIsImEiOiJjam13ZHlxbXgwdncwM3FvMnJjeGVubjI5In0.-ridMV6bkkyNhbPfMJhVzw')

#Set up web driver and base URL
#driver= webdriver.Chrome(executable_path='/Applications/chromedriver 3')

#Set base url (SAN FRANCISCO)
base_url = 'https://www.bandsintown.com/?place_id=ChIJIQBpAG2ahYAR_6128GcTUEo&page='#san francisco
#base_url = 'https://www.bandsintown.com/?place_id=ChIJOwg_06VPwokRYv534QaPC8g&page='


events = []
eventContainerBucket = []

for i in range(1,2):

    #cycle through pages in range
    driver.get(base_url + str(i))
    pageURL = base_url + str(i)

    # get events links
    event_list = driver.find_elements_by_css_selector('div[class^=_3buUBPWBhUz9KBQqgXm-gf] a[class^=_3UX9sLQPbNUbfbaigy35li]')
    # collect href attribute of events in even_list
    events.extend(list(event.get_attribute("href") for event in event_list))

print "total events: ", (len(events))

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}


# iterate through all events and open them.
item = {}
allEvents = []
for event in events:

    driver.get(event)
    currentUrl = driver.current_url
    print(currentUrl)
    try:
        currentRequest = requests.get(currentUrl, headers=headers)
        print (currentRequest)

        #print currentRequest.status_code
    except requests.exceptions.RequestException as e:
        print(e)
        continue


    if currentRequest.status_code == 200:
        #print ("link working")

        try:
            driver.find_element_by_css_selector('[class^=_3aZc11p4HaXXFyJp1e_XlL]')
            print "element exists!"
        except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
            print "element doesn't exist"
            pass

        # #Get Artist Name
        # artistNameContainer = driver.find_element_by_class_name('_2a7MPEB7nHW5q-0UQJsl6T')
        # artistName = artistNameContainer.text
        # print(artistName)
        #
        # # Get Venue
        # venueContainer = driver.find_element_by_class_name('_241_qbENUQasyRr7CHEJmo')
        # venueText = venueContainer.text
        # print(venueText)
        #
        # # Get Venue
        # venueSpecificContainer = driver.find_element_by_class_name('_1QjPq2P_9FMrK_-ZPAEgzQ')
        # venueSpecificText = venueSpecificContainer.text
        # print(venueSpecificText)
        #
        # # Get address
        # addressContainer = driver.find_element_by_class_name('_36ZCsgOz77AokAEvfUegFS')
        # addressText = addressContainer.text
        # print(addressText)
        #
        # # Get Date
        # dateContainer = driver.find_element_by_class_name('_1uSR2i2AbCWQwvNtGHdKnz')
        # dateText = dateContainer.text
        # print(dateText)
        #
        # # Get Time
        # timeContainer = driver.find_element_by_class_name('_1iK6x88EqsupILFxTvC9ip')
        # timeText = timeContainer.text
        # print(timeText)
        #
        # # Get Genre
        # genreContainer = driver.find_element_by_class_name('anCUcKviFIeXAPCRb8JZw')
        # genreText = genreContainer.text
        # print(genreText)




        soup = bs(driver.find_element_by_css_selector('[class^=_3aZc11p4HaXXFyJp1e_XlL]').get_attribute('outerHTML'))
        soup2 = bs(driver.find_element_by_css_selector('[class^=_3iav3Z5WtxzstYRQKmp3cW]').get_attribute('outerHTML'))

        #imageContainer = bs(driver.find_element_by_css_selector('[class^=_1tHUGDRLiXm3qKqo5etU7i]').get_attribute('outerHTML'))
        #aboutContainer = bs(driver.find_element_by_css_selector('[class^=_2U-3MMMCr9YL93ARQ21QrS]').get_attribute('outerHTML'))
        #print(aboutContainer)
        #containers = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')
        #date_time = containers[1].text.split('\n')
        print(soup)
        #print(soup2)
        # Only pull one weeks worth of data
        # Find date of event and format to compare against one week from now date
        #_1uSR2i2AbCWQwvNtGHdKnz

        #dateMatch = soup.select_one('img + div').text
        #test = soup.find('_1uSR2i2AbCWQwvNtGHdKnz').text
        #print(test)
        dateMatch = soup.select_one('._1uSR2i2AbCWQwvNtGHdKnz').text
        dateMatch = dateMatch.replace("th","")
        dateMatch = dateMatch.replace(".", "")
        dateMatch = dateMatch.replace(",", "")
        print(dateMatch)

        datetime_object = datetime.datetime.strptime(dateMatch, '%b %d %Y')
        datetime_object_str = datetime_object.strftime("%Y-%m-%d")
        print(datetime_object_str)
        # dateMatchSplit = dateMatch.split(',')
        # print("dateMatchSplit is: ", dateMatchSplit)
        # dateMatchDay = dateMatchSplit[1]
        # print("dateMatchDay is: ", dateMatchDay)
        # dateMatchCleaned = (re.sub(r'\D+$', '', dateMatchDay))
        # print("dateMatchCleaned is: ", dateMatchCleaned)
        # dateMatchDayFinal = (
        #         dateMatchSplit[0] + "," + dateMatchCleaned + "," + dateMatchSplit[2])
        # dateMatchDate = datetime.datetime.strptime(dateMatchDayFinal, '%A, %B %d, %Y')
        # eventDate = str(dateMatchDate).replace("00:00:00","")
        # eventDate = eventDate.rstrip()

        #print dateMatchDate, oneWeekDateTime

        #compare date of event to one week from now date
        if datetime_object <= oneWeekDateTime:
            print ("this event occurs one week or less from today")
            print("datetime object is", datetime_object)
            # Get artist
            #artist = soup2.select_one('h1').text
            artist = soup.select_one('._2a7MPEB7nHW5q-0UQJsl6T').text
            #artist = driver.find_element_by_class_name('_2a7MPEB7nHW5q-0UQJsl6T').text
            print(artist)

            # Get date
            #date = soup.select_one('img + div').text
            #dateSplit = date.split(',')
            #dateSplitDay = dateSplit[1]
            #dateSplitDayCleaned = (re.sub(r'\D+$', '', dateSplitDay))

            date = soup.select_one('._1uSR2i2AbCWQwvNtGHdKnz').text
            print(date)
            # #date = driver.find_element_by_class_name('_1uSR2i2AbCWQwvNtGHdKnz').text
            # dateSplit = date.split(',')
            # dateSplitDay = dateSplit[1]
            # dateSplitDayCleaned = (re.sub(r'\D+$', '', dateSplitDay))
            #
            # dSplit = dateSplitDayCleaned.split()
            # month = dSplit[0]
            # number = dSplit[1]
            #
            # dateFormatted = (dateSplit[0][0:3] + " " + month[0:3] + " " + number + dateSplit[2])
            # print(artist, dateFormatted)

            # Get time
            #time = soup.select_one('img + div + div').text
            #time = driver.find_element_by_class_name('_1iK6x88EqsupILFxTvC9ip').text
            time = soup2.select_one('._1iK6x88EqsupILFxTvC9ip').text
            print(time)

            # Get address
            #address = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div + div').text
            address= soup2.select_one('._36ZCsgOz77AokAEvfUegFS').text
            print(address)

            # Get venue
            venue = soup.select_one('._241_qbENUQasyRr7CHEJmo').text
            print(venue)

            #Get image
            #artistImage = imageContainer.select_one('img').get_attribute("src")
            artistImage = 'https://assets.prod.bandsintown.com/images/fallbackImage.png'
            try:
                artistImage = driver.find_element_by_xpath("//div[@class='_1tHUGDRLiXm3qKqo5etU7i']//img").get_attribute("src")
                print(artistImage)
            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                pass

            #Get genre information
            genre = 'No genre available'
            try:
                #genre = driver.find_element_by_xpath("//div[@class='_1Se_dqLEba70e_1AFsdzO3']").text
                #genre = driver.find_element_by_class_name('_1Se_dqLEba70e_1AFsdzO3').text
                listed_genres = driver.find_elements_by_xpath("//div[@class='_1Se_dqLEba70e_1AFsdzO3']")
                for str in listed_genres:
                    genre += (str.text + ',')
                genre = genre[:-1]
                print(genre)
                #genre = genreContainer.select_one('._1Se_dqLEba70e_1AFsdzO3').text
                #print(genre)
            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                pass

            #Get other information
            otherInfo = "No other event info available"
            try:
                otherInfo = driver.find_element_by_xpath("//div[@class='Wla7qETMG4RlwfQQMTIqx']").text
                print(otherInfo)
            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                pass



            # Get artist bio
            artistBio = "No artist bio available"
            try:
                artistBio = driver.find_element_by_xpath("//div[@class='VYokpSM2h3BWCLr3umXTd']").text
            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                pass

            # Capture additional bio info
            readMore = '_1XRy4PRswl0g1ImXMkYiQO'
            try:
                driver.find_element_by_xpath("//div[@class='_1XRy4PRswl0g1ImXMkYiQO']").click();
                #print(moreInfo)
            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                pass

            #Regardless of whether or not there is "Read More", print complete bio info.
            moreBioInfo = "No artist bio available"
            try:
                moreBioInfo = driver.find_element_by_xpath("//div[@class='VYokpSM2h3BWCLr3umXTd']").text
                print("more bio info is:", moreBioInfo)
            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                print('no moreBioInfo')
                pass



            #print artistBio, otherInfo, genre

            #Geocode address
            #geocodeInput = venue + ", " + address
            #print("geocode input is ", geocodeInput)
            #response = geocoder.google(address, key='AIzaSyCuC03rYbaH2WFQLy-4EO7qVSipEM84Iy4')
            #print(response)
            #result = response.json()
            #print(result)
            result = ''
            try:
                geolocator = Nominatim(user_agent="starrmoss1@gmail.com")
                result = geolocator.geocode(address)
                if result is None:
                    result = ''
                    pass
                else:
                    print((result.latitude, result.longitude))
                    coord_list = [result[1][0], result[1][1]]
                    print(coord_list)

            except (ElementNotVisibleException, NoSuchElementException, TimeoutException):
                print('no geocode possible')
                pass

            #create string for event date
            #datetime_object = str(datetime_object)

            #Bin information into 'item'
            item['Artist'] = artist
            item['Date'] = datetime_object_str
            item['eventDate'] = date
            item['Time'] = time
            item['Venue'] = venue
            item['Address'] = address
            item['artistImage'] = artistImage
            item['genre'] = genre
            item['otherInfo'] = otherInfo
            item['moreBioInfo'] = moreBioInfo
            #print(moreBioInfo)
            print(type(result))
            # Get latitude, longitude
            #coordinates = result['features'][0]['center']
            item['Coordinates'] = coord_list

            # Format output to JSON
            case = {'Artist': item['Artist'], 'Date': item['Date'], 'EventDate': item['eventDate'], 'Time': item['Time'], 'Venue': item['Venue'],
            'Address': item['Address'], 'Coordinates': coord_list, 'ArtistImage': item['artistImage'], 'Genre': item['genre'], 'otherInfo': item['otherInfo'], 'moreBioInfo': item['moreBioInfo']}

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

with open("/Users/starrmoss/Documents/nyc_events.json", "w") as writeJSON:
    file_str = json.dumps(allEvents, sort_keys=True)
    file_str = "var sf_events = " + file_str
    writeJSON.write(file_str)

print "Data pull complete!"