# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
import sys
import os
import time
import psycopg2

def download_stock_csv(code_range, save_dir):


    options = Options()
    # options.add_argument('--headless')

    #csvファイルの保存先を設定
    print('ファイル保存先: ' + str(save_dir))
    prefs = {"download.default_directory" : save_dir}
    options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(chrome_options=options)

    url = 'https://www.yahoo.co.jp/'
    driver.get(url)

    #ここで手動でログインを行う
    input('After login, press Enter:  ')

    for code_in_tuple in code_range:

        code = code_in_tuple[0]

        print("対象コード："+ str(code))

        #ファイル存在チェック
        if(isFileExist(code,save_dir)):
            print('既にDL済み')
            continue
    
        url = 'https://stocks.finance.yahoo.co.jp/stocks/history/?code={0}.T'.format(code)
        driver.get(url)

        try:
            driver.find_element_by_css_selector('#main > div.stocksCSVCenter > a > span.csvLinkText').click()

        except NoSuchElementException:
            print('csvがなかった。要確認 code: ' + str(code))
            pass

        time.sleep(2)

def select_brands_to_db():

    connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
    connection.get_backend_pid()
    cur = connection.cursor()

    sql = "SELECT code FROM brands"
    cur.execute(sql)
    return cur.fetchall()

def isFileExist(code, save_dir):
    filePath = save_dir + '/{0}.T.csv'.format(code)
    return os.path.exists(filePath)


if __name__ == '__main__':
    
    os.chdir('./csv')
    download_stock_csv(select_brands_to_db(),os.getcwd())
