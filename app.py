from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import os
import requests
from datetime import datetime
from urllib import parse

db_url = os.environ['DB_URL']
bot_token = os.environ['BOT_TOKEN']
date_key = 'date'
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
        # menu_items = MenuItem.query.all() # This works
        menu_items = MenuItem.query.filter(MenuItem.date == datetime.now().strftime('%Y-%m-%d')).all()
        menu_items = map(lambda m: {'date': m.date, 'type_of_meal': m.type_of_meal, 'name': m.name, 'dishes': m.dishes}, menu_items)
        pretty_menu_items = get_pretty(menu_items)
        print(pretty_menu_items)
        reply(chat_id, pretty_menu_items)
    else:
        reply(chat_id, 'Please type /start to start.')
    return 'OK'

def reply(chat_id, text):
    global bot_token
    text = parse.quote_plus(text)
    requests.get('https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'.format(bot_token, text, chat_id))

def get_pretty(menu_items):
    global name_key
    global dish_sep
    string_builder = ['Today\'s menu:\n']
    for menu_item in menu_items:
        string_builder.extend(['\n', menu_item[name_key], '\n'])
        if menu_item[dish_key]:
            dishes = menu_item[dish_key].split(dish_sep)
            for dish in dishes:
                string_builder.extend(['\t', dish, '\n'])
    if len(string_builder) == 1:
        string_builder.extend(['\n', 'N.A.', '\n'])
    return ''.join(string_builder)

if __name__ == '__main__':
    app.run()
