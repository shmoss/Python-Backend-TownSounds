import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib3, shutil

wiki_url = "https://en.wikipedia.org/wiki/List_of_best-charting_music_artists_in_the_United_States"
#r = requests.get(wiki_url, allow_redirects=True)
#print r.text
#soup = BeautifulSoup(r.text, "html.parser")
#print soup.prettify
#pageTitle = soup.find("title")
#print pageTitle.text

paragraphList = []

#for p in soup.select('p'):
    #print p.text
    #paragraphList.append(p.text)
#print paragraphList

df = pd.DataFrame()
df["paragraphList"] = paragraphList
df_file = pd.read_csv(r'/Users/starrmoss/Documents/Wiki_Test.csv')
#print df_file


paragraph = df_file["paragraphList"][1]
wordList = []


print paragraph.split()


#print wordList


