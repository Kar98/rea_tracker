
import csv
from tracker.rea_parser import ReaParser, backup_file

# This will merge the sold_main.txt into buy_main.txt.
# Run as a once off job if the get_sold.py fails.
output = 'D:/Coding/real_estate_tracker/output/'
buy_main = f'{output}buy_main.txt'
sold_main = f'{output}sold_main.txt'
buy_audit = f'{output}buy_audit.txt'

main_buy_record = ReaParser()
main_buy_record.load_from_csv(buy_main, buy_audit)
main_sold_record = ReaParser()
main_sold_record.load_from_csv(sold_main)

total_updated = 0
for mainrow in main_buy_record.articles:
    for soldrow in main_sold_record.articles:
        if mainrow.address == soldrow.address and mainrow.suburb == soldrow.suburb:
            mainrow.date_updated = soldrow.date_updated
            mainrow.agency = soldrow.agency
            mainrow.sale_date = soldrow.sale_date
            mainrow.sale_price = soldrow.sale_price
            mainrow.sold = soldrow.sold
            total_updated += 1

with open(buy_main, 'w', newline='') as csvfile:
    rea_writer = csv.writer(csvfile, delimiter='|')
    rea_writer.writerow(['Address', 'Suburb',  'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Auction', 'Date updated', 'Agent', 'Agency', 'Sale date', 'Sold price', 'soldflag'])
    for article in main_buy_record.articles:
        value = article.to_csv()
        rea_writer.writerow(value)

print('Total updated')
print(total_updated)