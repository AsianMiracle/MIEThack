#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[2]:


import bs4
from bs4 import BeautifulSoup


# In[3]:


import pandas as pd


# In[4]:


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


# In[5]:


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# In[ ]:





# In[6]:


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


# In[7]:


def parserRBC():
    html = get_html(URLRBC)
    if html.status_code == 200:
        cards = []
        html = get_html(URLRBC)
        cards.extend(get_contentRBC(html.text))
        return cards
    else:
        print('Error')


# In[8]:


parserRBC()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:


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


# In[10]:


def parserRIA():
    html = get_html(URLRIA)
    if html.status_code == 200:
        cards = []
        html = get_html(URLRIA)
        cards.extend(get_contentRIA(html.text))
        return cards
    else:
        print('Error')


# In[11]:


parserRIA()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[12]:


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


# In[13]:


def parserRT():
    html = get_html(URLRT)
    if html.status_code == 200:
        cards = []
        html = get_html(URLRT)
        cards.extend(get_contentRT(html.text))
        return cards
    else:
        print('Error')


# In[14]:


parserRT()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[15]:


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


# In[16]:


def parserVES():
    html = get_html(URLVES)
    if html.status_code == 200:
        cards = []
        html = get_html(URLVES)
        cards.extend(get_contentVES(html.text))
        return cards
    else:
        print('Error')


# In[17]:


parserVES()


# In[ ]:





# In[ ]:





# In[ ]:





# In[18]:


parRBC = parserRBC()
dfRBC = pd.DataFrame(parRBC)


# In[19]:


parRIA = parserRIA()
dfRIA = pd.DataFrame(parRIA)


# In[20]:


parRT = parserRT()
dfRT = pd.DataFrame(parRT)


# In[21]:


parVES = parserVES()
dfVES = pd.DataFrame(parVES)


# In[22]:


dfRBC


# In[23]:


dfRIA


# In[24]:


dfRT


# In[25]:


dfVES


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[26]:


def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)
tanimoto(dfRBC['title'][0], dfRIA['title'][0])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[27]:


da = dfRBC.title.tolist()
do = dfRIA.title.tolist()
for i in range(0, len(da)):
    for j in range(0, len(do)):
        print('da[i]=', da[i], 'do[j]=', do[j], '  ', fuzz.token_sort_ratio(da[i], da[j]))
        
        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




