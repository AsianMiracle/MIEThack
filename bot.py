import telebot
import config
import random
import requests
import Norm
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time
#import ParsStatCountry
#import ParsStatRegion
from sqlighter import SQLighter

from telebot import types


bot = telebot.TeleBot(config.TOKEN)
db = SQLighter('db.db')
sqlite3.connect(":memory:", check_same_thread = False)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Новостная рассылка")
item2 = types.KeyboardButton("Статистика по странам")

par = Norm.parser()
df = Norm.pd.DataFrame(par)
title = df.title.tolist()
link_title = df.link_title.tolist()

#par1 = ParsStatCountry.df.head(10).fillna('?')
#df1 = ParsStatCountry.pd.DataFrame(par1)
#country = df.columns['Страна'].tolist()
#ill = df.Всего_заражений.tolist()
@bot.message_handler(commands=['start'])
def welcome(message):    
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}. Это бот посвящен просмотру свежих новостей о COVID-19 и актуальной статисте".format(message.from_user, bot.get_me()),
    parse_mode='html', reply_markup=markup )

markup.add(item1, item2)



@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == 'Новостная рассылка':
			
			markup = types.InlineKeyboardMarkup(row_width=2)
			item3 = types.InlineKeyboardButton("Подписаться", callback_data='good')
			item4 = types.InlineKeyboardButton("Отписаться", callback_data='bad')

			markup.add(item3, item4)
			bot.send_message(message.chat.id,'Хочешь получать актуальную информацию о COVID-19? Подписывайся на информационную рассылку.', reply_markup=markup)

			
		elif message.text == 'Статистика по странам':
			bot.send_message(message.chat.id, 'Статистика заболеваний по странам: ')

		else:
			bot.send_message(message.chat.id, 'Повторите запрос')	




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message :
            if call.data == 'good':
                
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,text="Вы подписаны" )
                
                #удаление
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Хочешь получать актуальную информацию о COVID-19? Подписывайся на информационную рассылку.",reply_markup=None)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                while call.data == 'good':
                    bot.send_message(call.message.chat.id, title[0]+'\n'+link_title[0])
                    time.sleep(3600)
                    


         
              #  if(not db.subscriber_exists(call.message.from_user.id)):
                # если юзера нет в базе, добавляем его
              #     db.add_subscriber(call.this.message.from_user.id)
              #  else:
                 # если он уже есть, то просто обновляем ему статус подписки
               #    db.update_subscription(message.from_user.id, True)
                
            elif call.data == 'bad':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,text="Вы отписаны")
                #удаление
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Хочешь получать актуальную информацию о COVID-19? Подписывайся на информационную рассылку.",reply_markup=None) 
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)	

    except Exception as e:
        print(repr(e))






#RUN
bot.polling(none_stop=True)
