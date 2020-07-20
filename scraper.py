from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import os

# // TODO //

# Refactor to allow the collection on the innerhtml of the comments.
# Refactor so that final result is the full url from the href
# See lines 33, 44, and 45

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
        # As noted on line 38, we need to get href which requires this to be changed to innerhtml
        # comments[i] = comments[i].get_attribute('innerText')
        comments[i] = {"html": comments[i].get_attribute('innerHTML'), "text": comments[i].get_attribute('innerText')}
    return comments

def match_text(text):
    search_terms = ["Camera", "camera", "Cameras", "cameras", "construction camera", "construction cameras", "Construction camera", "Construction cameras", "construction cam", "Construction cam", "construction cams", "Construction cams", "Construction Cam", "Construction Cams", "Zeppelin"]
    return any(x in text for x in search_terms)

def find_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)

def filter_comments(comment_array, index):
    for i in range(len(comment_array)):
        cur_text = comment_array[i]["text"]
        if match_text(cur_text) and find_urls(cur_text):
            urls = comment_array[i]["html"].find_elements_by_xpath(".//a").get_attribute('href')
            # Now passing in index to allow us to collect the page number where the url was found. This will allow for easy collection of full urls even if the collected url is corrupted.
            # Many of the urls are collapsed, we need to find the href of the comments to get the full link.
            # urls = re.findall(r'(https?://[^\s]+)', comment_array[i])
            if len(urls) >= 1:
                return urls

for i in range(0, 1):
    driver.implicitly_wait(5)
    comments = collect_comments()
    url_list = filter_comments(comments, i)
    if url_list:
        results = results + url_list
    driver.get(base_url + str(i + 1))

print(results)

driver.close()
