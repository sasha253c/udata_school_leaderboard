# coding: utf-8

from collections import namedtuple

import requests
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TOKEN

Participant = namedtuple('Participant', ['place', 'username', 'math', 'python', 'total'])

URL = "https://quiz.udata.school/leaderboard/"
UA = UserAgent()

FIND_USERNAME = 'SashaKochyn'


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def getMyPlace():
    r = requests.get(URL, headers={'User-Agent': UA.random})
    # r = requests.get(URL, headers={
    #     'User-Agent': "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'"})
    bs = BeautifulSoup(r.text, 'lxml')
    participants = [Participant(*line.text.strip().split('\n')) for line in bs.find_all('table')[1].find_all('tr')]
    df = pd.DataFrame(participants)
    # df.set_index('place', inplace=True)
    df.replace({'N/A': 0}, inplace=True)
    for column in ('place', 'math', 'python', 'total'):
        df[column] = pd.to_numeric(df[column])

    length = len(df)
    my = Participant(**df[df['username'] == FIND_USERNAME].to_dict(orient='records')[0])
    return f'You are {my.place} from {length}'

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello')

def myPlaceCommand(bot, update):
    print('get command: get my place')
    message = getMyPlace()
    print('response')
    bot.send_message(chat_id=update.message.chat_id, text=message)

def textMessage(bot, update):
    response = 'Your message: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


if __name__ == '__main__':
    start_command_handler = CommandHandler('start', startCommand)
    myplace_command_handler = CommandHandler('myplace', myPlaceCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(myplace_command_handler)
    dispatcher.add_handler(text_message_handler)
    updater.start_polling(clean=True)
    # updater.idle()

    # print(getMyPlace())