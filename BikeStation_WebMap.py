#Dependencies

print 'Let google maps scraping commence!'

from bs4 import BeautifulSoup
import requests
import urllib3
from urllib3.util.retry import Retry
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#Set driver options
#Set driver options
options = Options()
options.add_argument('--no-sandbox') # Bypass OS security model
driverLocation = webdriver.Chrome(chrome_options=options, executable_path=r'/Applications/chromedriver 4')
driverLocation.quit()
driver= webdriver.Chrome(executable_path='/Applications/chromedriver 4')


s = requests.session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

base_url = 'https://www.google.com/maps/d/u/1/edit?mid=18mRYyiGL8k-QVciZMBDnGriCh10UUnTL&ll=37.77414573569942%2C-122.40467260417319&z=14'

driver.get('https://www.google.com/maps/d/u/1/edit?mid=18mRYyiGL8k-QVciZMBDnGriCh10UUnTL&ll=37.774141790813424%2C-122.40467260417319&z=14')
#currentRequest = requests.get(base_url)

driver.manage().timeouts().implicitlyWait(60, TimeUnit.SECONDS);


#artistImage = driver.find_element_by_xpath("//div[@class='i4ewOd-xl07Ob']")
driver.find_element_by_id("map-action-menu")
#print(artistImage)

#menu = soup.select_one('[class^=eventInfoContainer-2d9f07df]:nth-of-type(1) div').text

#map-action-menu

#i4ewOd-xl07Ob