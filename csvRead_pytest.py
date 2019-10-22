import csv
import glob
import datetime
import os

def generate_price_from_csv_file(csv_file_name, code):
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        next(reader) #先頭を飛ばす
        for row in reader:
            day = datetime.datetime.strptime(row[0], '%Y/%m/%d').date() #日付
            first = float(row[1]) #初値
            high = float(row[2]) #高値
            low = float(row[3]) #安値
            finish = float(row[4]) #終値
            value = float(row[5]) #出来高

            yield code, day, first, high, low, finish, value


def generate_from_csv_dir(csv_dir, generate_func):
    
    for path in glob.glob(os.path.join(csv_dir, "*.T.csv")):
        file_name = os.path.basename(path)
        code = file_name.split('.')[0]

        for d in generate_func(path, code):
            yield d
