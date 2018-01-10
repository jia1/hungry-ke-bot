from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import csv
import os
import requests
import time
from datetime import datetime

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

@app.route('/today', methods=['POST'])
def get_today_menu():
    req = request.get_json()
    print(req)
    if (not all(keys in ['update_id', 'message'] for keys in req)
        or not all(keys in ['chat', 'text'] for keys in req['message'])
        or not 'id' in req['message']['chat']):
        return 'Bad Request'
    update_id = req['update_id']
    chat_id = req['message']['chat']['id']
    message = req['message']['text']
    if message == '/start':
        menu_items = MenuItem.query.filter_by(date=datetime.today().date())
        pretty_menu_items = get_pretty(menu_items)
        print(pretty_menu_items)
        res = reply(chat_id, pretty_menu_items)
    else:
        res = reply(chat_id, 'Please type /start to start.')
    print(res)
    return res

def reply(chat_id, text):
    global bot_token
    res = requests.post(
        'https://api.telegram.org/bot{}/sendMessage'.format(bot_token),
        headers={'content-type': 'application/json'},
        data={'chat_id': chat_id, 'text': text})
    return res.json()

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
    return ''.join(string_builder)

if __name__ == '__main__':
    app.run()
