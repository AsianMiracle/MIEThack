#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import bs4
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
import re

HOSTRBC = 'https://www.rbc.ru/'
URLRBC = 'https://www.rbc.ru/story/5e2881539a794724ab627caa'
HOSTRIA = 'https://ria.ru/'
URLRIA = 'https://ria.ru/category_-koronavirus-covid-19/'
HOSTRT = 'https://russian.rt.com/'
URLRT = 'https://russian.rt.com/tag/koronavirus'
HOSTVES = 'https://www.vesti.ru/'
URLVES = 'https://www.vesti.ru/theme/2366'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_contentRBC(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    cards = []
    
    for item in items:
        cards.append(
            {
                'title': item.find('span', class_='item__title').get_text(strip=True),
                'link_title': item.find(class_='item__link').get('href'),
            }
        )
    return cards


def parserRBC():
    html = get_html(URLRBC)
    if html.status_code == 200:
        cards = []
        html = get_html(URLRBC)
        cards.extend(get_contentRBC(html.text))
        return cards
    else:
        print('Error')

parserRBC()

def get_contentRIA(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='list-item__content')
    cards = []
    
    for item in items:
        cards.append(
            {
                'title': item.find(class_='list-item__title').get_text(strip=True),
                'link_title': item.find(class_='list-item__title').get('href'),
            
            }
        )
    return cards

def parserRIA():
    html = get_html(URLRIA)
    if html.status_code == 200:
        cards = []
        html = get_html(URLRIA)
        cards.extend(get_contentRIA(html.text))
        return cards
    else:
        print('Error')


parserRIA()
def get_contentRT(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='listing__trend-right__wrapper')
    cards = []
    
    for item in items:
        cards.append(
            {
                'title': item.find(class_='trend-text-right').get_text(strip=True),
                'link_title': HOSTRT + item.find(class_='trend-text-right').find('a').get('href'),
            
            }
        )
    return cards

def parserRT():
    html = get_html(URLRT)
    if html.status_code == 200:
        cards = []
        html = get_html(URLRT)
        cards.extend(get_contentRT(html.text))
        return cards
    else:
        print('Error')
parserRT()

def get_contentVES(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='list__item')
    cards = []
    
    for item in items:
        cards.append(
            {
                'title': item.find(class_='list__title').get_text(strip=True),
                'link_product': HOSTVES + item.find(class_='list__pic-wrapper').get('href'),
            }
        )
    return cards

def parserVES():
    html = get_html(URLVES)
    if html.status_code == 200:
        cards = []
        html = get_html(URLVES)
        cards.extend(get_contentVES(html.text))
        return cards
    else:
        print('Error')
parserVES()
parRBC = parserRBC()
dfRBC = pd.DataFrame(parRBC)
parRIA = parserRIA()
dfRIA = pd.DataFrame(parRIA)
parRT = parserRT()
dfRT = pd.DataFrame(parRT)
parVES = parserVES()
dfVES = pd.DataFrame(parVES)
#print(dfRBC)
#print(dfRIA)
#print(dfRT)
#print(dfVES)

stop_words = stopwords.words('russian')
snowball = SnowballStemmer("russian")


def tokenizer(text):
    text = re.sub('<[^>]*>','',text)
    emoticons = re.findall(' (?::|;|=)(?:-)?(?:\)|\(|D|P) ',
                          text.lower())
    text = re.sub('[\W]+',' ', text.lower()) \
    + ' '.join(emoticons).replace('-','')
    tokenize = [w for w in text.split() if w not in stop_words]
    tokenized = [snowball.stem(word) for word in tokenize]
    return tokenized

so = []


da = dfRBC.title.tolist()
do = dfRIA.title.tolist()
for i in range(0, len(da)):
    for j in range(0, len(do)):
        if da[i] in so:
            continue
        else:
            if len(set(tokenizer(da[i]))&set(tokenizer(do[j]))) > 5:
                continue
            else:
                so.append(da[i])
                if do[j] == da[i]:
                    continue
                else:
                    if do[j] in so:
                        continue
                    else:
                        so.append(do[j])
#print(so)
#print(len(so))
doRT = dfRT.title.tolist()
so1 = []
for i in range(0, len(so)):
    for j in range(0, len(doRT)):
        if so[i] in so1:
            continue
        else:
            if len(set(tokenizer(so[i]))&set(tokenizer(doRT[j]))) >= 5:
                continue
            else:
                so1.append(so[i])
                if so[i] == doRT [j]:
                    continue
                else:
                    if doRT[j] in so1:
                        continue
                    else:
                        so1.append(doRT[j])

so2 = []
doVes = dfVES.title.tolist()
for i in range(0, len(so1)):
    for j in range(0, len(doVes)):
        if so1[i] in so2:
            continue
        else:
            if len(set(tokenizer(so1[i]))&set(tokenizer(doVes[j]))) > 5:
                continue
            else:
                so2.append(so1[i])
                if so1[i] == doVes[j]:
                    continue
                else:
                    if doVes[j] in so2:
                        continue
                    else:
                        so2.append(doVes[j])
dfRBC = pd.concat([dfRIA, dfRBC])
dfRBC = pd.concat([dfRT, dfRBC])
dfRBC = pd.concat([dfVES, dfRBC])
aa = dfRBC.title.tolist()
bb = dfRBC.link_title.tolist()
dictt = {k: bb.pop(0) for k in aa}
it = []
for g in range(0, len(so2)):
    nim = str(so2[g])
    a = dictt.get(str(nim))
    it.append(a)
itog = pd.DataFrame({'title' : so2,'link_title' : it})
print(itog.head())

#dfRBC = pd.concat([dfRIA, itog])