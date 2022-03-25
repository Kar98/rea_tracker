# from lib2to3.pgen2 import driver
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils import Utils

driver_path = 'E:\\Coding\\real_estate_tracker\\drivers'
sys.path.append(driver_path)
print(sys.path)

d = webdriver.Firefox()
utils = Utils(d)

def search_google(text):
    q = "//input[@name='q']"
    d.get('http://www.google.com.au')
    utils.wait(q)
    qe = d.find_element(By.XPATH, q)
    qe.send_keys(text)
    qe.send_keys(Keys.ENTER)

def get_google_link(name):
    links = d.find_elements(By.XPATH, "//h3")
    for link in links:
        if name in link.text:
            return link


search_google('realestate')
utils.wait('//h3')
time.sleep(1)
get_google_link('Search for Real Estate, Property & Homes').click()
# d.find_element(By.XPATH, '//h3').click()

# RE Page
re_search = "//input[@placeholder='Search suburb, postcode or state']"
re_done = "//button[contains(@aria-label, 'Close location')]"
re_search_btn = "//button[@aria-label='Apply filters']"
utils.wait(re_search)
el_search = d.find_element(By.XPATH, re_search)
el_search.click()
el_search.send_keys('Glenroy')
el_search.send_keys(Keys.DOWN)
el_search.send_keys(Keys.ENTER)
d.find_element(By.XPATH, re_done).click()
utils.wait(re_search_btn)
d.find_element(By.XPATH, re_search_btn).click()


d.close()
print('done')