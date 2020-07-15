from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import os

base_url = "https://forum.skyscraperpage.com/showthread.php?t=227316&page=1"

driver = webdriver.Firefox()
driver.get(base_url)
driver.implicitly_wait(100)

num_links = len(driver.find_elements_by_class_name('pagenavi'))

print(num_links)
