from tracker.rea_parser import ReaParser, backup_file
from os.path import abspath
output = 'D:/Coding/real_estate_tracker/output/'
buy_main = f'{output}buy_main.txt'
buy_audit = f'{output}buy_audit.txt'
sold_main = f'{output}sold_main.txt'

def write_sold_main(articles):
    outputstr = ''
    for a in articles:
        outputstr += f'{a.address}|{a.suburb}|{a.price}|{a.bedrooms}|{a.bathrooms}|{a.landsize}|{a.auction}|{a.date_updated}|{a.agent}|{a.agency}|{a.sale_date}|{a.sale_price}|{a.sold}\n'
    with open(sold_main+'t', 'w', newline='') as f:
        f.write(outputstr)

main_buy_record = ReaParser()
main_buy_record.get_from_csv(sold_main)

mini_sold = []
with open('D:/Coding/real_estate_tracker/output/collate/sold.txt', 'r') as f:
    mini_sold = f.readlines()

for row in mini_sold:
    splits = row.replace('\n','').split('|')
    address = splits[0]
    agent = splits[2]
    agency = splits[3]
    sale_date = splits[4]
    sale_price = splits[5]
    sold = splits[6]

    for article in main_buy_record.articles:
        if address == article.address:
            article.sale_date = sale_date
            article.sale_price = sale_price
            article.sold = sold
            break

write_sold_main(main_buy_record.articles)

