from pyquery import PyQuery
import time
import psycopg2
connection = psycopg2.connect("host=192.168.3.10 port=5432 dbname=stock_information user=postgres password=postgres")
connection.get_backend_pid()
connection.autocommit = True
cur = connection.cursor()
print(cur)

sql = "INSERT INTO brands (code,name,short_name,market,sector,unit) VALUES('0000','test','test','market','test',100)"
cur.execute(sql)


