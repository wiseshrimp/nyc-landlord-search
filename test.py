from bs4 import BeautifulSoup
from responseFunctions import *

raw_html = simple_get(
    'http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains')
html = BeautifulSoup(raw_html, 'html.parser')
for i, li in enumerate(html.select('li')):
  print(i, li.text)
