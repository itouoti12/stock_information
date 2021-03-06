# -*- coding: utf-8 -*-
from pyquery import PyQuery
import time
import sys
import re
import psycopg2
import datetime


def get_dailyData(code):

    print("対象コード：" + str(code))
    url = 'https://kabutan.jp/stock/?code={}'.format(code)

    q = PyQuery(url)

    if len(q.find('#stockinfo_b0')) == 0:
        return None

    try:

        date_value_raw = q.find('#kobetsu_left > h2:nth-child(2) > time').attr('datetime')
        date_value = datetime.datetime.strptime(date_value_raw, '%Y-%m-%d').date()

        open_value_raw = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)')[0].text
        open_value = float(open_value_raw.replace(',', ''))

        high_value_raw = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2)')[0].text
        high_value = float(high_value_raw.replace(',', ''))

        low_value_raw = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2)')[0].text
        low_value = float(low_value_raw.replace(',', ''))

        close_value_raw = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2)')[0].text
        close_value = float(close_value_raw.replace(',', ''))

        volume_value_raw = q.find('#kobetsu_left > table:nth-child(4) > tbody > tr:nth-child(1) > td')[0].text
        volume_str = re.search(u'.*(?=株)', volume_value_raw)
        volume_value = float(volume_str.group(0).replace(',', ''))


    except ValueError:
        return None

    except:
        print("多分上場廃止してる")
        return None

    print(code)
    print(date_value)
    print(open_value)
    print(high_value)
    print(low_value)
    print(close_value)
    print(volume_value)
    return code, date_value, open_value, high_value, low_value, close_value, volume_value 


def daily_generator(code_range):
    for code_in_tuple in code_range:
        code = code_in_tuple[0]

        daily = get_dailyData(code)

        if daily:
            yield daily

        time.sleep(2)


def insert_daily_to_db(code_range):

    connection = psycopg2.connect(
        "host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    connection.autocommit = True
    with connection.cursor() as cur:

        for daily in daily_generator(code_range):

            sql = "INSERT INTO raw_prices (code,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"

            try:
                cur.execute(sql, daily)

            except psycopg2.errors.UniqueViolation:
                print("すでに登録済み")

def select_brands_to_db():

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    with connection.cursor() as cur:

        sql = "SELECT code FROM brands WHERE deleted = 0"
        cur.execute(sql)
        return cur.fetchall()

if __name__ == '__main__':
    args = sys.argv
    insert_daily_to_db(select_brands_to_db())