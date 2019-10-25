from pyquery import PyQuery
import time
import sys

def get_brand(code):
    q = PyQuery("https://kabutan.jp/stock/?code=7203")
    sector = q.find('#stockinfo_i2 > div > a')[0].text
    print(sector)
    print(code)

if __name__ == '__main__':
    args = sys.argv
    get_brand(args[1])

    
