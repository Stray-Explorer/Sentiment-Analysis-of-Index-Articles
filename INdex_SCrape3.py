#!/home/d0c/Environments/Sent/bin/python
# coding: utf-8

import time
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
import os
from tkinter import *
import textwrap


while True:
    
    stop_words = nltk.corpus.stopwords.words('hungarian')
    #print(stop_words)
    xtrastops = ['Atv.hu', 'arra', 'három', 'ezer', 'is.', 'meg,', 'be', 'volt,', 'Ez', 'Phelps', 'van,', 'Ha', 'Azt', 'is', 'A', 'Az', '-', '–', 'is ', 'ha', 'is,', 'is,', 'És', 'De', 'Miatt', 'miatt', 'van', 'My', 'BuzzFeed', 'két', 'ki,', 'ő']
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




    os.environ["DISPLAY"] = ":1.0"


    dexres = open('DEXresults.txt', 'r')
    lines = dexres.readlines()
    content = []
    for line in range((len(lines)-9), len(lines)-1):
        content.append(lines[line])
    #print(content[1:7])
    #print(content[2])
    #print(content[3])

    #mostwords = ' '.join(content[5:6])
    mostwords = content[0]
    #print(mostwords)
    sentres = ' '.join(content[1:7])# + ' '.join(content[-2:])
    #sentres = ' '.join(content[0:4]) + ' '.join(content[-2:])
    mostwords_wrapped = textwrap.fill(mostwords, width = 45) 
    sentres_wrapped = textwrap.fill(sentres, width = 45)
    dexres.close()

    DexRs = Tk()

    DexRs.title('Sentiment Analysis of Index Articles')
    DexRsContentWords = Label(DexRs, text= mostwords_wrapped)
    DexRsContentRes = Label(DexRs, text= sentres_wrapped)

    DexRsContentWords['bd'] = 16
    #DexRsContentWords['relief'] = 'ridge'
    DexRsContentWords['font'] = 'Mistral 17 bold'
    DexRsContentWords['bg'] = 'black'
    DexRsContentWords['fg'] = 'green'
    DexRsContentWords['text'] = mostwords_wrapped
    DexRsContentWords['padx'] = 16


    DexRsContentRes['bd'] = 16
    DexRsContentRes['relief'] = 'ridge'
    DexRsContentRes['font'] = 'Mistral 17 bold'
    DexRsContentRes['bg'] = 'black'
    DexRsContentRes['fg'] = 'green'
    DexRsContentRes['text'] = sentres_wrapped
    DexRsContentRes['padx'] = 12

    

    DexRs.after(885000, lambda: DexRs.destroy())
    
    DexRsContentWords.pack()
    DexRsContentRes.pack(expand=True)
    
    DexRs.mainloop()
#    DexRs.destroy() 885000



    

    














