# -*- coding: utf-8 -*-
from pyquery import PyQuery
import time
import sys
import re
import psycopg2

def update_brands_to_db(code_range):

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    connection.autocommit = True
    with connection.cursor() as cur:

        for code_in_tapple in code_range:
            code = code_in_tapple[0]

            print("対象コード："+ code)

            sql = "UPDATE brands SET deleted = 1 WHERE code = %s"
            
            try:
                cur.execute(sql,code_in_tapple)

            except psycopg2.errors.UniqueViolation:
                print("すでに登録済み")


def select_delete_brands():

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    with connection.cursor() as cur:

        sql = "SELECT code FROM delete_brands WHERE date <= CURRENT_DATE"
        cur.execute(sql)
        return cur.fetchall()

if __name__ == '__main__':
    args = sys.argv
    update_brands_to_db(select_delete_brands())
        

    


    
