import json
from tracker.rea_parser import ReaParser
parser = ReaParser()

parser.get_from_csv('./output/sold_main.txt')
for article in parser.articles:
    if article.suburb == 'Glenroy':
        if article.sold != '1' and article.sold != '0':
            print(article.address + '  ' + article.sold)
