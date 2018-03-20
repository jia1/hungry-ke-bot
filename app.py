from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

import os
import requests
from datetime import datetime
from pytz import timezone
from urllib import parse

db_url = os.environ['DB_URL']
bot_token = os.environ['BOT_TOKEN']
date_key = 'date'
meal_key = 'type_of_meal'
name_key = 'name'
dishes_key = 'dishes'
dishes_string_separator = ','

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Silence the deprecation warning
db = SQLAlchemy(app)

from models import MenuItem # Import after everything else, otherwise circular dependency

sentry = Sentry(app) # Must export SENTRY_DSN

@app.route('/')
def index():
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
    chat_id = req['message']['chat']['id']
    message = req['message'].get('text', '')
    if message == '/start':
        today = datetime.now(timezone('Asia/Singapore')).date()
        menu_items = [{meal_key: menu_item.type_of_meal, name_key: menu_item.name, dishes_key: menu_item.dishes} for menu_item in MenuItem.query.all()
            if menu_item.date.date() == today]
        meals = [
            filter(lambda menu_item: menu_item[meal_key] == 'breakfast', menu_items),
            filter(lambda menu_item: menu_item[meal_key] == 'dinner', menu_items),
        ]
        pretty_menu_items = get_pretty(meals)
        reply(chat_id, pretty_menu_items)
    else:
        reply(chat_id, 'Please type /start to start.')
    return 'OK'

def reply(chat_id, text):
    text = parse.quote_plus(text)
    requests.get('https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'.format(bot_token, text, chat_id))

def get_pretty(meals, meal_types=['breakfast', 'dinner']):
    string_builder = ['Today\'s menu:']
    for i in range(len(meals)):
        string_builder.append('\n\n**{meal}**'.format(meal=meal_types[i].capitalize()))
        menu_items = meals[i]
        if not menu_items:
            string_builder.append('\nN.A.')
            continue
        for index, menu_item in enumerate(menu_items, ord('A')):
            string_builder.append('\n{index}. {name}'.format(index=chr(index), name=menu_item[name_key].capitalize()))
            if menu_item[dishes_key]:
                dishes = menu_item[dishes_key].split(dishes_string_separator)
                for index, dish in enumerate(dishes, 1):
                    string_builder.append('\n    {index}. {dish}'.format(index=index, dish=dish.capitalize()))
    return ''.join(string_builder)

if __name__ == '__main__':
    app.run()
