import csv
import os

DATA_PTH = os.path.dirname(os.path.abspath(__file__)).split('hiroko')[0] + 'hiroko/data/'


def csvRead(file, filepth=DATA_PTH, delimiter=';'):
    with open(filepth + file, newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=delimiter)
        return list(csv_data)[1:]
