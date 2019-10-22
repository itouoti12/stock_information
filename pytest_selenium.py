from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


url = 'https://jp.kabumap.com/servlets/kabumap/Action?SRC=basic/top/base&codetext=7203'
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)
unit = driver.find_element_by_css_selector('#minUnit').text
print(unit)