import sys
from datetime import datetime
debug = False
if __name__ == "__main__":
    sys.path.append("D:\\Coding\\real_estate_tracker")

if debug == False:
    with open(f'./latest.txt', 'r') as fread:
        content = fread.readline()
        if datetime.now().strftime("%d/%m/%Y") == content:
            print(f'Already run for {content}')
            sys.exit()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from tracker.utils import Utils
CSS = By.CSS_SELECTOR
XPATH = By.XPATH
driver_path = 'D:\\Coding\\real_estate_tracker\\drivers\\chromedriver.exe'
sys.path.append(driver_path)
options = Options()
if debug == False:
    # pass
    options.add_argument("--headless=new")
d = webdriver.Chrome(options=options, executable_path="D:\\Coding\\real_estate_tracker\\drivers\\chromedriver.exe")
utils = Utils(d)

def type(text):
    for key in text:
        input.send_keys(key)
        time.sleep(0.4)


def click(locator, nth=0):
    if '/' in locator:
        by = By.XPATH
    else:
        by = By.CSS_SELECTOR
    utils.wait(locator, by)
    try:
        d.find_elements(by, locator)[nth].click()
    except:
        print(f'Could not click element {locator}')
        d.get_screenshot_as_file('./err.png')
        raise Exception(f'Could not click element {locator}')

def search_google(text):
    q = "[title=Search]"
    d.get('http://www.google.com.au')
    utils.wait(q,By.CSS_SELECTOR)
    qe = d.find_element(By.CSS_SELECTOR, q)
    qe.send_keys(text)
    qe.send_keys(Keys.ENTER)

    
def get_google_link(name):
    links = d.find_elements(By.XPATH, "//h3")
    for link in links:
        if name in link.text:
            return link
# RE Page
search = "//div[contains(@data-testid,'typeahead') and @role='button']"
input = "[placeholder='Try a location or a school or project name ']"
search_btn = "//span[text()='Search']"
filters = "//span[text()=' Filters']"
clear_filter = "[data-testid=buy-navigation]"
nearby = "//div[text()='Search nearby suburbs']"
featured = "[data-testid='sort-by-section'] [role=combobox]"
dropdown = "#search-results-sort-by-filter-item-1"
paginator = "[data-testid='paginator-navigation-button']"
# Navigate
search_google('domain')
utils.wait('//h3')
time.sleep(1)
get_google_link('Domain.com').click()
# REA navigation
utils.wait(search)
el_search = d.find_element(XPATH, search)
el_search.click()
input = d.find_element(CSS, input)
# Search
type('glenroy')
input.send_keys(Keys.ENTER)
# Click filters and remove popup
click(filters)
time.sleep(1)
click(clear_filter, 1)
time.sleep(1)
click(nearby)
time.sleep(1)
count = len(d.find_elements(XPATH, search_btn))
d.find_elements(XPATH, search_btn)[count-2].click()
time.sleep(1)
click(featured)
time.sleep(1)
click(dropdown)
time.sleep(3)
# Start main loop
filenum = 1
while True:
    with open(f'./pages/buy/dom-g{filenum}.html', 'w', encoding='utf-8') as fwrite:
        source = d.find_element(CSS, "[data-testid='page']").get_attribute('outerHTML')
        fwrite.write(source)
        print(f'Wrote file dom-g{filenum}.html')
    if d.find_elements(CSS, paginator)[1].get_dom_attribute('disabled') is not None:
        break
    click(paginator, 1)
    filenum += 1
    if filenum > 8:
        print('Total files exceeded 8, a problem may have occurred')
        break
    time.sleep(8)
    
d.close()
print('done')

