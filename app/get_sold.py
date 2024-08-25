import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tracker.rea_parser import ReaParser, backup_file
from os.path import abspath

# *** Sold processing ***
# Need to set PYPATH first : $env:PYTHONPATH="D:\Coding\real_estate_tracker"
# Get all pages in sold and put them into a list
# Then write out that list to the disk
# Then Load up the buy-main and see if a sold record exists for a buy. If it does, match the 2 together and save them.
# Write out the properties that sold and for what price.

# Install selenium
d = webdriver.Chrome()
d.set_page_load_timeout(10)

# Grab list of properties to search for
output = 'D:/Coding/real_estate_tracker/output/'
buy_main = f'{output}buy_main.txt'
buy_audit = f'{output}buy_audit.txt'
sold_main = f'{output}sold_main.txt'
error_file = './output/errors.txt'
d.implicitly_wait(1)


def get_single_article(articles, name):
    for article in articles:
        if article.address == name:
            return article

def element_exists(locator):
    try:
        d.find_element(By.CSS_SELECTOR, locator)
        return True
    except:
        return False

def select_search_result():
    WebDriverWait(d, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='More results']")))
    google_results = d.find_elements(By.XPATH, "//h2[not(contains(@class,'footer'))]")

    for result in google_results:
        if article.address in result.text:
            result.click()
            WebDriverWait(d,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#domain-logo-wrapper"))) # Wait for domain logo to display
            return True
    return False

def get_details(article):
    # Search google and get first result
    WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=q]")))
    query = d.find_element(By.CSS_SELECTOR, 'input[name=q]')
    # Sometimes REA stuff up address and put in 2 whitespaces
    if '  ' in article.address:
        address = article.address.replace('  ', ' ')
    else:
        address = article.address
    query.send_keys(f'site:www.domain.com.au {address}, {article.suburb}')
    query.send_keys(Keys.ENTER)

    if(select_search_result() == False):
        return ['no_search_result','no_search_result','-1']

    is_property_profile = False
    if 'property-profile' in d.current_url:
        is_property_profile = True
    

    try:
        # There are 2 types of pages. Property profile and Sold. Sometimes the search index picks up a different page and so different elements need to be parsed.
        if is_property_profile:
            ActionChains(d).move_to_element(d.find_element(By.XPATH, "//figure/../../div/div")).perform()
            WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tab-Sold'] > button"))).click()
            time.sleep(1)
            date = d.find_element(By.XPATH, "//figure/../../div/div").text.replace('\n','-')
            price = d.find_element(By.CSS_SELECTOR, "span[data-testid=fe-co-property-timeline-card-heading]").text
            if('not sold' in price):
                sold = 0
            else:
                sold = 1
        else:
            WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='listing-details__summary-title']")))
            title_element = d.find_element(By.CSS_SELECTOR, "[data-testid='listing-details__summary-title']").text
            if 'SOLD' in title_element:
                # split on title
                title_split = title_element.split(' - ')
                price = title_split[1]
                # Date is in different element
                listing_tag = d.find_element(By.CSS_SELECTOR, "[data-testid='listing-details__listing-tag']").text
                tag_split = []
                if 'auction ' in listing_tag:
                    tag_split = listing_tag.split('auction')
                elif 'treaty ' in listing_tag:
                    tag_split = listing_tag.split('treaty')
                date = tag_split[1]
                sold = 1
            elif 'leased' in title_element:
                return ['none','to_be_rent','2']
            else:
                raise Exception('Not property profile and not sold')

            
        
    except Exception as e:
        print(e)
        print(article.address)
        date = 'unknown_date'
        price = 'unknown_price'
        sold = 0
        if element_exists("li > h5"):
            return ['none','no_sale_data','0']
        if element_exists("div[class=listing-details__root]"):
            return ['none','to_be_sold','0']
        if element_exists("button[data-testid=header__back-button]"):
            el = d.find_element(By.CSS_SELECTOR, "button[data-testid=header__back-button]").text
            if(' sale ' in el):
                return ['none','to_be_sold','0']
            elif(' rent ' in el):
                return ['none','to_be_rent','0']
    
    return [date,price,f'{sold}']


def write_sold_main(articles):
    outputstr = ''
    for a in articles:
        outputstr += f'{a.address}|{a.suburb}|{a.price}|{a.bedrooms}|{a.bathrooms}|{a.landsize}|{a.auction}|{a.date_updated}|{a.agent}|{a.agency}|{a.sale_date}|{a.sale_price}|{a.sold}\n'
    with open(sold_main, 'w', newline='') as f:
        f.write(outputstr)

# Clear previous error file
with open(error_file, 'w') as f:
    f.write('')

main_buy_record = ReaParser()
main_buy_record.load_from_csv(buy_main)


sold_records = []
error_records = []

# Go to search engine
d.get("https://duckduckgo.com")
d.maximize_window()

articles = main_buy_record.articles

# Get the sold details
max_iterations = 0
start_pos = 1

for x in range(start_pos,len(articles)):
    article = articles[x]
    if(max_iterations == 500):
        print('Max iterations hit')
        break
    if article.suburb == 'Glenroy' and ('to_be_sold' in article.sale_price or len(article.sold) == 0):
        print(f'Processing {article.address}')
        try:
            details = get_details(article)
            #sold_records.append(details)
            article.sale_date = details[0]
            article.sale_price = details[1]
            article.sold = details[2]
            print(details)
        except Exception as e:
            print(e)
            details = f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|unknown_date|unknown_price|\n'
            #error_records.append(article.address)
            #sold_records.append(details)
            article.sale_date = 'unknown_date'
            article.sale_price = 'unknown_price'
            article.sold = ''
            print(f'Error - {article.address}')
            with open(error_file, 'a', newline='') as f:
                f.write(details)
        
        write_sold_main(articles)
        try:
            d.get("https://duckduckgo.com")
        except Exception as e:
            print(e)
            print('Error with going to search engine. Attempting to recover.')
        time.sleep(5) # Too fast and google starts captcha
        max_iterations += 1

main_sold_record = ReaParser()
main_sold_record.load_from_csv(sold_main)
# After all the listings have been searched, get the sold file and merge the changes back onto buymain. 
# A new sold file is created because if it errors I don't want to lose the results. I constantly write to the sold file, 
# then I can merge the changes across at any point.
for mainrow in main_buy_record.articles:
    for soldrow in main_sold_record.articles:
        if mainrow.address == soldrow.address and mainrow.suburb == soldrow.suburb:
            mainrow.date_updated = soldrow.date_updated
            mainrow.agency = soldrow.agency
            mainrow.sale_date = soldrow.sale_date
            mainrow.sale_price = soldrow.sale_price
            mainrow.sold = soldrow.sold

with open(buy_main, 'w', newline='') as csvfile:
    rea_writer = csv.writer(csvfile, delimiter='|')
    rea_writer.writerow(['Address', 'Suburb',  'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Auction', 'Date updated', 'Agent', 'Agency', 'Sale date', 'Sold price', 'soldflag'])
    for article in main_buy_record.articles:
        value = article.to_csv()
        rea_writer.writerow(value)

d.close()
d.quit()

