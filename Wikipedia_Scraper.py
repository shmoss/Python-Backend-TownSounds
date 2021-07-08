#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib3, shutil
import string
#import json
#import geocoder

#import selenium
#from selenium import webdriver

#from selenium import webdriver
#from bs4 import BeautifulSoup as bs



###########Download a webpage to a Local HTML file ################

web_url = 'https://en.wikipedia.org/wiki/List_of_Asian_countries_by_area'
r = requests.get(web_url, allow_redirects=True)
open('google2.html', 'wb').write(r.content)


# This is one way to get text
wiki = BeautifulSoup(r.text, "html.parser")
for i in wiki.select('p'):
    print i.getText()

# this is a very similar way
page_url = '/Users/starrmoss/PycharmProjects/hi/google2.html'
wiki_soup = BeautifulSoup(open(page_url).read())
#print wiki_soup.text
for i in wiki_soup.select('p'):
    print i.getText()


My_table_1 = wiki_soup.find('table',{'class':'wikitable sortable'})
print My_table_1

##########  Scrape Wikipedia Soccer Table ###########

league_url = requests.get("https://en.wikipedia.org/wiki/1999%E2%80%932000_FA_Premier_League").text
league_soup = BeautifulSoup(league_url, "html")
league_all_tables = league_soup.findAll("table")

right_table = league_soup.findAll("table", class_ = "wikitable sortable")[1]


print right_table

A = []
B = []
C = []
D = []
E = []

for row in right_table.findAll('tr'):
    league_cells = row.findAll('td')
    if len(league_cells)==5:
        A.append(league_cells[0].get_text(strip=True))
        B.append(league_cells[1].get_text(strip=True))
        C.append(league_cells[2].get_text(strip=True))
        D.append(league_cells[3].get_text(strip=True))
        E.append(league_cells[4].get_text(strip=True))


league_df = pd.DataFrame()
league_df['Team'] = A
league_df['Manager'] = B
league_df['Captain'] = C
league_df['Kit Manufacturer'] = D
league_df['Shirt Sponsor'] = E

print league_df
league_df.to_csv(r'/Users/starrmoss/Documents/league_DF.csv')

########## Download a .txt file from a link ##########


http = urllib3.PoolManager()

MTA_url = requests.get("http://web.mta.info/developers/turnstile.html").text

MTA_soup = BeautifulSoup(MTA_url)

MTA_soup.findAll('a')
one_a_tag = MTA_soup.findAll("a")[36]
MTA_link = one_a_tag["href"]
print(MTA_link)

download_url = 'http://web.mta.info/developers/'+ MTA_link
print download_url
#open('google.ico', 'wb').write(MTA_link.content)
out_file = '/Users/starrmoss/Documents/test_output_download.csv'

res = http.request('GET', download_url, preload_content=False)
out_file = open(out_file, 'wb')
shutil.copyfileobj(res, out_file)


############ Scrape Wikipedia County by Area Table #################


print 'Lets Scrape Wikipedia!'

# Access url, return HTML
website_url = requests.get("https://en.wikipedia.org/wiki/List_of_Asian_countries_by_area").text

soup = BeautifulSoup(website_url)

My_table = soup.find('table',{'class':'wikitable sortable'})


links = My_table.findAll('a')
table_data = My_table.findAll('td')

Countries = []
for link in links:
    Countries.append(link.get('title'))

df = pd.DataFrame()
df['Country'] = Countries

df.to_csv(r'/Users/starrmoss/Documents/test_DF.csv')

#print df


############ Scrape Wikipedia Incarceration Table #############


table = soup.findAll('table')[1]
rows = table.findAll('tr')
#print rows

first_columns = []
third_columns = []
second_columns = []

for row in rows[1:]:
    first_columns.append(row.findAll('td')[0].get_text(strip=True))
    second_columns.append(row.findAll('td')[1].get_text(strip=True))
    third_columns.append(row.findAll('td')[2].get_text(strip=True))


df2 = pd.DataFrame()
df2['first_column'] = first_columns
df2['second_column'] = second_columns
df2['third_column'] = third_columns

#print df2

df2.to_csv(r'/Users/starrmoss/Documents/Countries_DataFrame.csv')


############ Third Example, extracting information from US incarceration rates table


incarceration_url = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_incarceration_rate').text

incarceration_soup = BeautifulSoup(incarceration_url)
#print incarceration_soup

incarceration_table = incarceration_soup.find('table',{'class':'wikitable nowrap sortable'})
print incarceration_table
print "incarceration table"
incarceration_rows = incarceration_table.findAll('tr')

col_one = []
col_two = []
col_three = []

for row in incarceration_rows[1:]:
    col_one.append(row.findAll('td')[0].get_text(strip=True))
    col_two.append(row.findAll('td')[1].get_text(strip=True))
    col_three.append(row.findAll('td')[2].get_text(strip=True))

df3 = pd.DataFrame()
df3['col_one'] = col_one
df3['col_two'] = col_two
df3['col_three'] = col_three


df3.to_csv(r'/Users/starrmoss/Documents/Incarceration_DataFrame.csv')



print "script has ended"