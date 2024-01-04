import time
import re
from selenium.webdriver.common.by import By
from tracker.rea_parser import ReaParser, backup_file
from datetime import datetime, date

rea = ReaParser()

test = """
some data
here
not
"""

val = re.search("some data.*(.*?).*not", test, re.DOTALL)


articles = rea.parse_domain_buy_page('./pages/buy/dom-g5.html')
for article in articles:
    print(article.to_csv())

print(len(articles))
