#!/usr/bin/env python
# coding: utf-8

import requests

import bs4
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

HOST = 'https://www.rbc.ru/'
URL = 'https://www.rbc.ru/story/5e2881539a794724ab627caa'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_content(html):
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
def parser():
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        html = get_html(URL)
        cards.extend(get_content(html.text))
        return cards
    else:
        print('Error')


par = parser()
df = pd.DataFrame(par)


