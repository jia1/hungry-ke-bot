from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import os
import requests
from datetime import datetime
from pytz import timezone
from urllib import parse
import psycopg2 # To import tz

db_url = os.environ['DB_URL']
bot_token = os.environ['BOT_TOKEN']
date_key = 'date'
meal_key = 'type_of_meal'
name_key = 'name'
dish_key = 'dishes'
dish_sep = ','

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Silence the deprecation warning
db = SQLAlchemy(app)

from models import MenuItem # Import after everything else, otherwise circular dependency

@app.route('/')
def index():
    print(db_url)
    print(bot_token)
    return 'Hello, World!'

# Example webhook payload
'''
{
    'message': {
        'text': 'ok',
        'message_id': 13,
        'chat': {
            'type': 'private',
            'id': 132455911,
            'first_name': 'Jia Yee'
        },
        'date': 1515607534,
        'from': {
            'language_code': 'en-SG',
            'id': 132455911,
            'first_name': 'Jia Yee',
            'is_bot': False
        }
    },
    'update_id': 508520474
}
'''

@app.route('/{}'.format(bot_token), methods=['POST'])
def get_today_menu():
    req = request.get_json()
    print(req)
    chat_id = req['message']['chat']['id']
    message = req['message']['text']
    print(chat_id)
    print(message)
    if message == '/start':
        menu_items = MenuItem.query.all() # This works
        menu_items = map(lambda m: {date_key: m.date, meal_key: m.type_of_meal, name_key: m.name, dish_key: m.dishes}, menu_items)
        menu_items = list(filter(is_today, menu_items))
        print(list(menu_items))

        string_builder = ['Today\'s menu:\n']
        print(menu_items)
        for menu_item in menu_items:
            print(menu_item)
            string_builder.extend(['\n', menu_item[date_key], '\n'])
            string_builder.extend(['\n', menu_item[meal_key], '\n'])
            string_builder.extend(['\n', menu_item[name_key], '\n'])
            if menu_item[dish_key]:
                dishes = menu_item[dish_key].split(dish_sep)
                for dish in dishes:
                    string_builder.extend(['\t', dish, '\n'])
        print(string_builder)
        if len(string_builder) == 1:
            string_builder.extend(['\n', 'N.A.', '\n'])
        pretty_menu_items = ''.join(string_builder)

        # pretty_menu_items = get_pretty(list(menu_items))
        print(pretty_menu_items)
        reply(chat_id, pretty_menu_items)
    else:
        reply(chat_id, 'Please type /start to start.')
    return 'OK'

def is_today(menu_item):
    print(menu_item[date_key], menu_item[date_key].date())
    print(datetime.now(timezone('Asia/Singapore')), datetime.now(timezone('Asia/Singapore')).date())
    print(menu_item[date_key].date() == datetime.now(timezone('Asia/Singapore')).date())
    return menu_item[date_key].date() == datetime.now(timezone('Asia/Singapore')).date()

def reply(chat_id, text):
    text = parse.quote_plus(text)
    requests.get('https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'.format(bot_token, text, chat_id))

def get_pretty(menu_items):
    string_builder = ['Today\'s menu:\n']
    print(menu_items)
    for menu_item in menu_items:
        print(menu_item)
        string_builder.extend(['\n', menu_item[date_key], '\n'])
        string_builder.extend(['\n', menu_item[meal_key], '\n'])
        string_builder.extend(['\n', menu_item[name_key], '\n'])
        if menu_item[dish_key]:
            dishes = menu_item[dish_key].split(dish_sep)
            for dish in dishes:
                string_builder.extend(['\t', dish, '\n'])
    print(string_builder)
    if len(string_builder) == 1:
        string_builder.extend(['\n', 'N.A.', '\n'])
    return ''.join(string_builder)

if __name__ == '__main__':
    app.run()
