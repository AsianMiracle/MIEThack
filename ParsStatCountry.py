#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import requests

HW = 'https://index.minfin.com.ua/reference/coronavirus/geography/'


def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r
html = get_html(HW)
table = pd.read_html(html.text)
df7 = pd.DataFrame(table[0])
df7 = df7.drop(df7.head(2).index).reset_index(drop=True)
df7.columns = ['Страна', 'Всего_заражений', 'Заражений за сутки', 'Смертельные случаи', 'Смертей за сутки', 'Выздоровело', 'Выздоровело за сутки', 'Больные']
print(df7.head(10).fillna('?'))

