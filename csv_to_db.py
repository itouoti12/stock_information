# -*- coding: utf-8 -*-

import csv
import glob
import datetime
import os
import psycopg2
import codecs

def generate_price_from_csv_file(csv_file_name,code):

    # with open(csv_file_name) as file:
    with codecs.open(csv_file_name, 'r', 'utf-8', 'ignore') as file:
        reader = csv.reader(file)
        # 先頭行を飛ばす
        next(reader)

        for row in reader:
            date_value = datetime.datetime.strptime(row[0], '%Y/%m/%d').date()
            open_value = float(row[1])
            high_value = float(row[2])
            low_value = float(row[3])
            close_value = float(row[4])
            volume_value = float(row[5])

            yield code, date_value, open_value, high_value, low_value, close_value, volume_value

def generate_from_csv_dir(generate_func):
    
    os.chdir('./csv')
    for path in glob.glob(os.path.join(os.getcwd(), "*.T.csv")):
        file_name = os.path.basename(path)
        code = file_name.split('.')[0]
        
        for dir in generate_func(path, code):
            yield dir

def all_csv_file_to_db():
    price_generator = generate_from_csv_dir(generate_price_from_csv_file)


    for price in price_generator:

        connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
        connection.get_backend_pid()
        connection.autocommit = True
    
        with connection.cursor() as cur:

            sql = "INSERT INTO raw_prices (code,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            
            try:
                cur.execute(sql,price)

            except psycopg2.errors.UniqueViolation:
                print("すでに登録済み")


if __name__ == '__main__':
    all_csv_file_to_db() 
        