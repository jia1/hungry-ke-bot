import csv
import sys

csv_file_path = sys.argv[1]

with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    columns = list(filter(None, next(reader)))
    # Assert number of columns
    # Assert column names
    last_column_index = len(columns) - 1
    for csv_row in reader:
        values = csv_row[:last_column_index]
        # Assert date time format
        dishes = csv_row[last_column_index:]
        # Assert no comma in each dish
        # This is a possible indication that multiple dishes will be read as one dish

