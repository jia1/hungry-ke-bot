import csv
import sys

csv_file_path = sys.argv[1]

with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    columns = list(filter(None, next(reader)))
    print(columns)
    last_column_index = len(columns) - 1
    for csv_row in reader:
        values = csv_row[:last_column_index]
        date_value = values[0]
        print(date_value)
        dishes = list(filter(None, csv_row[last_column_index:]))
        print(dishes)

