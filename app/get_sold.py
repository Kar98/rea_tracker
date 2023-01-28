import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tracker.rea_parser import ReaParser, backup_file
from os.path import abspath


# Install selenium
d = webdriver.Chrome()

# Grab list of properties to search for
output = 'D:/Coding/real_estate_tracker/output/'
buy_main = f'{output}buy_main.csv'
buy_audit = f'{output}buy_audit.txt'
sold_main = f'{output}sold_main.txt'
sold_file = './output/sold.txt'
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

def select_google_result():
    element = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.XPATH, "//h3")))
    google_results = d.find_elements(By.XPATH, "//h3[not(@role)]")

    for result in google_results:
        if article.address in result.text:
            result.click()
            return True
    return False

def get_details(article):
    # Search google and get first result
    WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=q]")))
    query = d.find_element(By.CSS_SELECTOR, 'input[name=q]')
    query.send_keys('site:www.domain.com.au '+article.address+', '+article.suburb)
    query.send_keys(Keys.ENTER)

    if(select_google_result() == False):
        return f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|unknown|no_google_res|0\n'


    try:
        ActionChains(d).move_to_element(d.find_element(By.XPATH, "//figure/../../div/div")).perform()
        WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tab-Sold'] > button"))).click()
        time.sleep(1)
        date = d.find_element(By.XPATH, "//figure/../../div/div").text.replace('\n','-')
        price = d.find_element(By.CSS_SELECTOR, "span[data-testid=fe-co-property-timeline-card-heading]").text
        if('not sold' in price):
            sold = 0
        else:
            sold = 1
    except Exception as e:
        #print(e)
        date = 'unknown_date'
        price = 'unknown_price'
        sold = 0
        if element_exists("li > h5"):
            return f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|none|no_sale_data|0\n'
        if element_exists("div[class=listing-details__root]"):
            return f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|none|to_be_sold|0\n'
        if element_exists("button[data-testid=header__back-button]"):
            el = d.find_element(By.CSS_SELECTOR, "button[data-testid=header__back-button]").text
            if(' sale ' in el):
                return f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|none|to_be_sold|0\n'
            elif(' rent ' in el):
                return f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|none|to_be_rent|0\n'
    
    return f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|{date}|{price}|{sold}\n'


def write_sold_main(articles):
    outputstr = ''
    for a in articles:
        outputstr += f'{a.address}|{a.suburb}|{a.price}|{a.bedrooms}|{a.bathrooms}|{a.landsize}|{a.auction}|{a.date_updated}|{a.agent}|{a.agency}|{a.sale_date}|{a.sale_price}|{a.sold}\n'
    with open(sold_main, 'w', newline='') as f:
        f.write(outputstr)

# Clear output files
with open(sold_file, 'w') as f:
    f.write('')
with open(error_file, 'w') as f:
    f.write('')

main_buy_record = ReaParser()
main_buy_record.get_from_csv(sold_main)
sold_records = []
error_records = []

# Go to google
d.get("http://www.google.com")
d.maximize_window()

articles = main_buy_record.articles

for article in articles:
    if article.suburb == 'Glenroy' and (article.sold == ''):
        try:
            details = get_details(article)
            sold_records.append(details)
        except:
            details = f'{article.address}|{article.suburb}|{article.agent}|{article.agency}|unknown_date|unknown_price|\n'
            error_records.append(article.address)
            sold_records.append(details)
            print(f'Error - {article.address}')
            with open(error_file, 'a', newline='') as f:
                f.write(details)
        
        write_sold_main(articles)
        d.get("http://www.google.com")
        time.sleep(5) # Too fast and google starts captcha



d.close()
d.quit()

