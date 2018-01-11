'''
upload.py is a Python script that loads data from a local CSV file to a Postgres database

To be executed externally (because of Heroku's ephemeral file system)

Usage in command line:
$ export DB_URL=<database URL>
$ python upload.py menu.csv
'''

from datetime import datetime
import csv
import psycopg2
import os
import sys

db_url = os.environ['DB_URL']
csv_file_path = sys.argv[1]

connection = psycopg2.connect(db_url)
with connection:
    with connection.cursor() as cursor:
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            columns = list(filter(None, next(reader)))
            last_column_index = len(columns) - 1
            print(columns, last_column_index)
            for csv_row in reader:
                values = csv_row[:last_column_index]
                values[0] = datetime.strptime(csv_row[0], '%d/%m/%Y')
                if not csv_row[last_column_index]:
                    cursor.execute('INSERT INTO menu_items (date, type_of_meal, name) VALUES (%s, %s, %s)', values)
                else:
                    dishes = filter(None, csv_row[last_column_index:len(csv_row)])
                    values.append(','.join(dishes))
                    cursor.execute('INSERT INTO menu_items (date, type_of_meal, name, dishes) VALUES (%s, %s, %s, %s)', values)
                print(values)
    connection.commit()
