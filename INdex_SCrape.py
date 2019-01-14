#!/home/d0c/Environments/Sent/bin/python
# coding: utf-8


import importlib
import datetime
import io
import nltk
import re
import string
from csv import writer
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import json
import sys


stop_words = nltk.corpus.stopwords.words('hungarian')
#print(stop_words)
xtrastops = ['Atv.hu', 'arra', 'három', 'ezer', 'is.', 'meg,', 'be', 'volt,', 'Ez', 'Phelps', 'van,', 'Ha', 'Azt', 'is', 'A', 'Az', '-', '–', 'is ', 'ha', 'is,', 'is,', 'És', 'De', 'Miatt', 'miatt', 'van', 'My', 'BuzzFeed', 'két']
stop_words.extend(xtrastops)
#print(stop_words)
#timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%m-%d %H:%M')
headers = {'User-Agent': 'Mozilla/5.0'}
''' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0 '''


dex = open('dexscrape.txt', 'a+')    
target_site = requests.get('https://index.hu', headers = headers, timeout = 5)
if target_site.status_code == 200:
    soup = BeautifulSoup(target_site.text, 'lxml')


#Ez a resz kiveszi a cikk URL-t.
    for href in soup.find_all('h1', {'class': ['cikkcim']})[0:8]:
        url = href.a.get('href')
        cikkszoveg = requests.get(url, headers = headers, timeout = 5)
        soup2 = BeautifulSoup(cikkszoveg.text, 'lxml')
        cikkszoveg = requests.get(url, headers = headers, timeout = 5)
        soup2 = BeautifulSoup(cikkszoveg.text, 'lxml')
        for cikkparagrafusok in soup2.find_all('p')[0:-6]:
            dex.write(cikkparagrafusok.get_text())
# Ez a resz kiirja a fooldalon levo cikk cimet es ajanlojat.
    for cikkcim_ajanlo in soup.find_all(True, {'class': ['cikkcim', 'ajanlo']})[0:8]:
        dex.write(cikkcim_ajanlo.get_text())
dex.close()



dex = open('dexscrape.txt', 'r+')
line = dex.read()
words = line.split()
#print(words)
dextokens = [word for word in words if not word in stop_words]
#print(dextokens)
dexres = open('DEXresults.txt', 'a+')
Dexfreqdist = FreqDist(dextokens)
dexres2 = (Dexfreqdist.most_common(25))

sentanalysistxt = []
for (a, b) in dexres2:
    sentanalysistxt.append(a)
sentanalysistxt = ' '.join(sentanalysistxt)
#entanalysistxt = sentanalysistxt.encode('utf-8')
t = json.dumps(sentanalysistxt) #, ensure_ascii=False)#.encode('utf-8')
#print(type(t))

headers = {
    'Content-Type':'application/json; charset=utf-8', 
}

data = '{"sentence": %s}'
data = data % t
#data = data.encode('latin-1')
#print(data)
response = requests.post('http://172.17.0.1:5000/sentiment', headers = headers, data = data)
sentiment_result = response.json()
response.keep_alive = False
#print(sentiment_result)
for key, value in sentiment_result.items():
    sentdic = value[0]
    

dexres2 = str(dexres2)
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime('%m-%d  %H:%M')
dexres2 = '\r\r\n' + dexres2 + '\n'
dexres.write(dexres2)




for i, j in sentdic.items():
    dexres.write(str(i) + '\r\n')
    dexres.write(str(j) + '\r\n')

dexres.write(str(timestamp) + '\r\n' + '\r\n')
    
       

open('dexscrape.txt', 'w')
dex.close()
dexres.close()
















