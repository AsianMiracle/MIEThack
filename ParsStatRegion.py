#!/usr/bin/env python
# coding: utf-8

# In[324]:


import pandas as pd
import requests

H = 'https://horosho-tam.ru/rossiya/coronavirus'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
html = get_html(H)
table = pd.read_html(html.text)
df = pd.DataFrame(table[0])
df = df.drop(df.head(1).index).reset_index(drop=True)


# In[325]:


def clean_cell(s):
    for i in range(len(s)):
        if (s[-i] == '+'):
            s = s[:-i]
            break
    return s


# In[326]:


zrz = df['Заразилось'].tolist()
newzrz = []
for s in zrz:
    if type(s) != float:
        a = clean_cell(s)
        newzrz.append(a)
df['Заразилось'] = pd.Series(newzrz)

mrl = df['Умерло'].tolist()
newmrl = []
for s in mrl:
    if type(s) != float:
        a = clean_cell(s)
        newmrl.append(a)
df['Умерло'] = pd.Series(newmrl)

vzdr = df['Выздоровело'].tolist()
newvzdr = []
for s in vzdr:
    if type(s) != float:
        a = clean_cell(s)
        newvzdr.append(a)
df['Выздоровело'] = pd.Series(newvzdr)


# In[327]:


print(df)


# In[397]:


def find(co):
    out = df.loc[df['Регион'] == co]
    for index, row in out.iterrows():
        print(row['Заразилось'], row['Умерло'], row['Летальность'], row['Выздоровело'], sep ='\n')


# In[398]:


find('')


# In[ ]:




