from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import csv
import requests
import time
from datetime import datetime
from configparser import ConfigParser

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

app = Flask(__name__)

postgres = dict(config.items('postgres'))
DATABASE_URI = 'postgresql+psycopg2://{username}:{password}@{host}/{database}'.format(
    user=postgres['username'],
    password=postgres['password'],
    host=postgres['host'],
    database=postgres['database'])
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Silence the deprecation warning

date_key = config.get('script', 'date_key')
name_key = config.get('script', 'name_key')
dish_key = config.get('script', 'dish_key')
dish_sep = config.get('script', 'dish_string_separator')

db = SQLAlchemy(app)

from models import MenuItem

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/load')
def load_csv():
    global config
    global config_file
    global date_key
    global dish_key
    global dish_sep
    if config.getboolean('data', 'should_load'):
        with open(config.get('data', 'FILE'), newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            column_names = next(csv_reader)
            num_columns = len(column_names)
            for menu_item_list in csv_reader:
                menu_item_dict = {}
                for i in range(len(menu_item_list[:num_columns])):
                    column_name = column_names[i]
                    menu_item_dict[column_name] = menu_item_list[i]
                menu_item_dict[date_key] = datetime.strptime(
                    menu_item_dict[date_key],
                    config.get('script', 'date_format_string')).date()
                menu_item_dict[dish_key] = [menu_item_dict[dish_key]]
                for dish in menu_item_list[num_columns:]:
                    menu_item_dict[dish_index].append(dish)
                menu_item_dict[dish_key] = separator.join(menu_item_dict[dish_index])
                db.session.add(MenuItem(**menu_item_dict))
        db.session.commit()
        config.set('data', 'should_load', 'no')
        with open(data_file, 'w') as config_file:
            config.write(config_file)
        return 'Created'
    else:
        return 'Forbidden'

@app.route('/today', methods=['POST'])
def get_today_menu():
    req = request.get_json()
    if (not all(keys in ['update_id', 'message'] for keys in req)
        or not all(keys in ['chat', 'text'] for keys in req['message'])
        or not 'id' in req['message']['chat']):
        return 'Bad Request'
    update_id = req['update_id']
    chat_id = req['message']['chat']['id']
    message = req['message']['text']
    if message == '/start':
        menu_items = MenuItem.query.filter_by(date=datetime.today().date())
        res = reply(chat_id, get_pretty(menu_items))
    else:
        res = reply(chat_id, 'Please type /start to start.')
    return res

def reply(chat_id, text):
    res = requests.post(
        'https://api.telegram.org/bot{}/sendMessage'.format(config.get('bot', 'token')),
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
