# -*- coding: utf-8 -*-
from pyquery import PyQuery
import time
import sys
import re
import psycopg2
import datetime


def get_selectdays_data(code,day):

    print("対象コード：{} 対象日付:{}".format(str(code), day))

    url = 'https://kabuoji3.com/stock/{}/{}/'.format(code, day.year)
    q = PyQuery(url)

    if len(q.find("tr:contains('{}') > td:nth-child(1)".format(day))) == 0:
        return None

    try:

        open_value_raw = q.find(
            "tr:contains('{}') > td:nth-child(2)".format(day))[0].text
        open_value = float(open_value_raw)

        high_value_raw = q.find(
            "tr:contains('{}') > td:nth-child(3)".format(day))[0].text
        high_value = float(high_value_raw)

        low_value_raw = q.find(
            "tr:contains('{}') > td:nth-child(4)".format(day))[0].text
        low_value = float(low_value_raw)

        close_value_raw = q.find(
            "tr:contains('{}') > td:nth-child(5)".format(day))[0].text
        close_value = float(close_value_raw)

        volume_value_raw = q.find(
            "tr:contains('{}') > td:nth-child(6)".format(day))[0].text
        volume_value = float(volume_value_raw)


    except ValueError:
        return None

    except:
        print("多分上場廃止してる")
        return None

    print(code)
    print(day)
    print(open_value)
    print(high_value)
    print(low_value)
    print(close_value)
    print(volume_value)
    return code, day, open_value, high_value, low_value, close_value, volume_value


def daily_generator(code_range,start_date,end_date):
    for code_in_tuple in code_range:
        code = code_in_tuple[0]

        for day in range((end_date - start_date).days + 1):

            daily = get_selectdays_data(code, start_date + datetime.timedelta(day))

            if daily:
                yield daily

            time.sleep(2)

def insert_daily_to_db(code_range,start_date,end_date):

    connection = psycopg2.connect(
        "host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    connection.autocommit = True
    with connection.cursor() as cur:

        for daily in daily_generator(code_range,start_date,end_date):

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

    
    start_date = datetime.datetime.strptime(args[1], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(args[2], '%Y-%m-%d').date()

    insert_daily_to_db(select_brands_to_db(),start_date,end_date)
