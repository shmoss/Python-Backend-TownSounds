#Import the necessary methods from tweepy library

print 'hi'

from bs4 import BeautifulSoup
import requests
import json
import geocoder
import selenium
from selenium import webdriver



#This simulates page-clicks using Selenium
#Simulate page-click for each event to grab address
driver = webdriver.Chrome(executable_path='/Applications/chromedriver')
# Go to your page url
#driver.get('https://www.bandsintown.com/?came_from=257&page=71')
#button_element = driver.find_element_by_class_name('eventList-5e5f25ca')
#button_element.click()

#uniqueAddress = find_all('div', {'class': 'eventInfoContainer-2d9f07df'})
#print uniqueAddress


#Test - help from stackOverflow

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
for event in events:
    driver.get(event)
    uniqueEventContainer = driver.find_elements_by_css_selector('div[class^=eventInfoContainer-]')
    print uniqueEventContainer[0].text
    #uniqueEventContainerHMTL = uniqueEventContainer.get_attribute('innerHTML')
    #print uniqueEventContainerHMTL
    eventContainerBucket.append(uniqueEventContainer)

print eventContainerBucket

#for i in eventContainerBucket:
    #print i.get_attribute('innerHTML')

page = 'https://www.bandsintown.com/?came_from=257&page='
urlBucket = []
for i in range (0,3):
    uniqueUrl = page + str(i)
    urlBucket.append(uniqueUrl)

#print urlBucket

responseBucket = []
driverBucket = []
buttonBucket = []

for i in urlBucket:
    uniqueResponse = requests.get(i)
    responseBucket.append(uniqueResponse)
    drivers = driver.get(i)
    allelements = len(driver.find_elements_by_class_name('eventList-5e5f25ca'))
    #for index in range((allelements)-1):
        #driver.find_elements_by_class_name("eventList-5e5f25ca")[index].click()


    print allelements

    driverBucket.append(drivers)


    #for i in driverBucket:
       # button_element = driver.find_elements_by_class_name('eventList-5e5f25ca')
       #print button_element





#for i in driverBucket:


#print driverBucket
    #for i in driverBucket:
        #button_element = driver.find_element_by_class_name('eventList-5e5f25ca')
        #button_element.click()
        #print button_element


#print responseBucket

soupBucket = []
for i in responseBucket:
    individualSoup = BeautifulSoup(i.text, 'html.parser')
    soupBucket.append(individualSoup)


#print soupBucket

uniqueDatesBucket = []
for i in soupBucket:
   uniqueDate = i.find_all('div', {'class': 'event-b58f7990'})
   uniqueDatesBucket.append(uniqueDate)
   #print (uniqueDate)

#print uniqueDatesBucket
#print (len(uniqueDatesBucket))
uniqueMonth = []
uniqueDates = []

uniqueMonthDayBucket = []

uniqueBandNameBucket = []
for i in soupBucket:
   uniqueBandName = i.find_all('div', {'class': 'event-38a9a08e'})
   uniqueBandNameBucket.append(uniqueBandName)
   #print (uniqueDate)

#print uniqueBandNameBucket

bandNames = []
for entry in uniqueBandNameBucket:
    for band in entry:
        uniqueBand = band.find_all('h2')[0].get_text()
        #print uniqueBand
        #text = uniqueBand.next_element
        #print text
        #uniqueBand.append(bandNames)

#print bandNames

for udb in uniqueDatesBucket:
    for i in udb:
        uniqueMonthDay = i.find_all('div')

        uniqueMonth.append('Month' + uniqueMonthDay[0].text)
        uniqueDates.append('Month: ' + uniqueMonthDay[0].text + ' ' + 'Day: ' + uniqueMonthDay[1].text)

#print uniqueDates
array = [
'https://www.bandsintown.com/?came_from=257&sort_by_filter=Number+of+RSVPs&page=',
'https://www.bandsintown.com/?came_from=257&sort_by_filter=Number+of+RSVPs&page=2',
'https://www.bandsintown.com/?came_from=257&sort_by_filter=Number+of+RSVPs&page=3',
'https://www.bandsintown.com/?came_from=257&sort_by_filter=Number+of+RSVPs&page=4'
]
#print array
url = 'https://www.bandsintown.com/?came_from=257&sort_by_filter=Number+of+RSVPs&page=1'
response = requests.get(url)

for thing in array:
    response2 = requests.get(thing)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    #print soup2
    dates = soup2.find_all('div', {'class': 'event-b58f7990'})


soup = BeautifulSoup(response.text, 'html.parser')
#print soup
for i in soup.find('div', {'class': 'event-b58f7990'}).find_all('div'):

    #print (i.text)
    x=1


dates = soup.find_all('div', {'class': 'event-b58f7990'})
#print(len(dates))
#print (dates)
month=[]
day=[]
for i in dates:
    md = i.find_all('div')
    month.append(md[0].text)
    day.append(md[1].text)
    #print(md)


entries = []
for i in soupBucket:
   item = {}
   uniqueEntry = i.find_all('div', {'class': 'event-0fe45b3b'})
   #print uniqueEntry
   #uniqueEntry.append(entries)
   for i in uniqueEntry:
       bandEntry = i.find_all('div', {'class': 'event-38a9a08e'})
       dateEntry = i.find_all('div', {'class': 'event-b58f7990'})
       #print dateEntry
       #print bandEntry
      # entries.append('Artist: ' + bandEntry)



       for i in bandEntry:
           name = i.find_all('h2')[0].get_text()
           #print name
           venueInfo = i.find_all('div', {'class': 'event-a7d492f7'})
           venueText = venueInfo[0].text
           #print venueText
           for i in venueInfo:
               venueDiv = i.find_all('div', {'class': 'event-6891d84c'})
               locationDiv = i.find_all('div', {'class': 'event-c5863c62'})
               venue = venueDiv[0].text
               location = locationDiv[0].text
               #entries.append('Artist: ' + name + 'Venue: ' + venue + ' ' + 'location: ' + location)
               item['Artist'] = name
               item['Venue'] = venue
               item['Location'] = location
               #entries.append(item)
               #print("Artist: " + item['Artist'])
               #print("Venue: " + item['Venue'])
               #print("Location: " + item['Location'])
               uniqueLocation = (venue + "," + location)
               g = geocoder.google('Mountain View, CA', key='AIzaSyCuC03rYbaH2WFQLy-4EO7qVSipEM84Iy4')
               print location
               #print geocodedLocation
               #print "unique location is" + uniqueLocation
               #latLong = 'https://maps.googleapis.com/maps/api/geocode/json?address=' +[uniqueLocation] + '&sensor=true'
              # print latLong
               #print venue
               #print location
               #location = venueInfo[1].text
           #venue = venueText[1]
           #print venue
           #location = venueInfo[1].text

           for i in venueInfo:
              venue = i.find_all('div', {'class': 'event-6891d84c'})
              location = i.find_all('div', {'class': 'event-c5863c62'})

              #uniqueVenue = venue.text


           #print name

       for i in dateEntry:
           date = i.find_all('div')
           month = date[0].text
           day = date[1].text
           #print day
           #print month
           #entries.append('Artist: ' + name + 'Month: ' + month + 'Day: ' + day)
           item['Day'] = day
           item['Month'] = month
           print("Day: " + item['Day'])
           print("Month: " + item['Month'])



#print entries

with open("textbooks5.json", "w") as writeJSON:
   json.dump(item, writeJSON, ensure_ascii=False)
    #for uniqueDate = i.find_all('div', {'class': 'event-b58f7990'})
    #print (uniqueDate)



print ('end')
#event-b58f7990
#eventList-5e5f25ca
# in unique date bucket --- class="event-ad736269"
# event-38a9a08e  - container
# event-5daafce9 - band name
# event-a7d492f7  1st element in child - venue, 2nd element in child - city,State

