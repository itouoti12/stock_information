# -*- coding: utf-8 -*-

from pyquery import PyQuery
import datetime
import psycopg2

def new_barnds_generator():
    url = 'https://www.jpx.co.jp/listing/stocks/new/index.html'
    page = PyQuery(url) 

    for d, i in zip(page.find('tbody > tr:even > td:eq(0)'), page.find('tbody > tr:even span')):

        date = datetime.datetime.strptime(d.text, '%Y/%m/%d').date()
        yield (i.get('id'), date)

def insert_new_brands_to_db():

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    connection.autocommit = True
    with connection.cursor() as cur:

        for brand in new_barnds_generator():

            sql = "INSERT INTO new_brands (code,date) VALUES(%s,%s)"
            
            try:
                cur.execute(sql,brand)

            except psycopg2.errors.UniqueViolation:
                print("すでに登録済み")

if __name__ == '__main__':
    insert_new_brands_to_db()
        