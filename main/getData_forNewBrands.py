# -*- coding: utf-8 -*-
from pyquery import PyQuery
import time
import sys
import re
import psycopg2

def get_brand(code):
    
    code = code[0]
    print("対象コード："+ str(code))
    url = 'https://kabutan.jp/stock/?code={}'.format(code)

    q = PyQuery(url)

    if len(q.find('#stockinfo_b0')) == 0:
        return None

    try:
        name = re.search('(?<=^.{4}).*',q.find('#stockinfo_i1 > div.si_i1_1 > h2').text())

        short_name_target = q.find('#header > div.fs0 > div > ol > li:nth-child(2) > span')[0].text
        short_name = re.search('.*(?=\()',short_name_target)
        
        market = q.find('#stockinfo_i1 > div.si_i1_1 > span')[0].text
        
        unit_str_target = q.find('#stockinfo_i2 > dl:nth-child(3) > dd')[0].text
        unit_str = re.search(u'.*(?=株)',unit_str_target)
        unit = int(unit_str.group(0))
        
        sector = q.find('#stockinfo_i2 > div > a')[0].text
    

    except ValueError:
        return None

    except:
        print("多分上場廃止してる")
        return None
    
    print(code)
    print(name.group(0))
    print(short_name.group(0))
    print(market)
    print(sector)
    print(unit)
    return code, name.group(0), short_name.group(0), market, sector,unit

def brands_generator(code_range):
    for code in code_range:
        brand = get_brand(code)

        if brand:
            yield brand
        
        time.sleep(2)

def insert_brands_to_db(code_range):

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    connection.autocommit = True
    with connection.cursor() as cur:

        for brand in brands_generator(code_range):

            sql = "INSERT INTO brands (code,name,short_name,market,sector,unit) VALUES(%s,%s,%s,%s,%s,%s)"
            
            try:
                cur.execute(sql,brand)

            except psycopg2.errors.UniqueViolation:
                print("すでに登録済み")


def select_new_brands():

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    with connection.cursor() as cur:

        sql = "SELECT code FROM new_brands WHERE date <= CURRENT_DATE"
        cur.execute(sql)
        return cur.fetchall()

if __name__ == '__main__':
    args = sys.argv
    insert_brands_to_db(select_new_brands())
        

    


    
