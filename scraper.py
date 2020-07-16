from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import os

base_url = "https://forum.skyscraperpage.com/showthread.php?t=227316&page="

driver = webdriver.Firefox()
driver.get(base_url + "1")
driver.implicitly_wait(10)

link_wrapper = driver.find_elements_by_class_name('pagenavi')[0]
num_buttons = link_wrapper.find_elements_by_xpath(".//div")[1]
max_page_num = num_buttons.find_elements_by_xpath(".//a")[7].get_attribute('innerText')
max_expected_wait = int((int(max_page_num) * 5) / 60)

print("Maximum wait time: " + str(max_expected_wait) + " minutes")

results = []

def collect_comments():
    comments = driver.find_elements_by_css_selector("div[id*='post_message']")
    for i in range(len(comments)):
        comments[i] = comments[i].get_attribute('innerText')
    return comments

def match_text(text):
    search_terms = ["Camera", "camera", "Cameras", "cameras", "construction camera", "construction cameras", "Construction camera", "Construction cameras", "construction cam", "Construction cam", "construction cams", "Construction cams", "Construction Cam", "Construction Cams", "Zeppelin"]
    return any(x in text for x in search_terms)

def filter_comments(comment_array):
    for i in range(len(comment_array)):
        if match_text(comment_array[i]):
            urls = re.findall(r'(https?://[^\s]+)', comment_array[i])
            if len(urls) >= 1:
                return urls

for i in range(0, int(max_page_num) + 1):
    driver.implicitly_wait(5)
    comments = collect_comments()
    url_list = filter_comments(comments)
    if url_list:
        results = results + url_list
    driver.get(base_url + str(i + 1))

print(results)

driver.close()
