from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from tqdm import tqdm
import re
import os

# // TODO //

# Create .csv file with the urls and page number rather than printing it.


base_url = "https://forum.skyscraperpage.com/showthread.php?t=227316&page="

driver = webdriver.Firefox()
driver.get(base_url + "1")
driver.implicitly_wait(10)

link_wrapper = driver.find_elements_by_class_name('pagenavi')[0]
num_buttons = link_wrapper.find_elements_by_xpath(".//div")[1]
max_page_num = num_buttons.find_elements_by_xpath(".//a")[7].get_attribute('innerText')

results = []

def grab_href(link_list):
    links = []
    for i in range(len(link_list)):
        links.append(link_list[i].get_attribute('href'))
    return links

def collect_comments():
    comments = driver.find_elements_by_css_selector("div[id*='post_message']")
    for i in range(len(comments)):
        comments[i] = {"links": grab_href(comments[i].find_elements_by_xpath(".//a")), "text": comments[i].get_attribute('innerText')}
    return comments

def match_text(text):
    search_terms = ["Camera", "camera", "Cameras", "cameras", "construction camera", "construction cameras", "Construction camera", "Construction cameras", "construction cam", "Construction cam", "construction cams", "Construction cams", "Construction Cam", "Construction Cams"]
    return any(x in text for x in search_terms)

def find_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)

def filter_comments(comment_array, index):
    for i in range(len(comment_array)):
        cur_text = comment_array[i]["text"]
        if match_text(cur_text) and find_urls(cur_text):
            urls = comment_array[i]["links"]
            if len(urls) >= 1:
                return urls

for i in tqdm(range(0, int(max_page_num) + 1)):
    driver.implicitly_wait(5)
    comments = collect_comments()
    url_list = filter_comments(comments, i)
    if url_list:
        results = results + url_list
    driver.get(base_url + str(i + 1))

print(results)

driver.close()
