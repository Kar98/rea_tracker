import os
import csv
import sys
import json
import shutil
import time
from datetime import datetime
from tracker.rea_parser import ReaParser, backup_file

# TODO: Run as a webapp
# TODO: Load sold pages in and check what price it sold for vs what it listed
# TODO: Find out which places sold


buy_pages = 'D:/Coding/real_estate_tracker/pages/buy/'
sold_pages = 'D:/Coding/real_estate_tracker/pages/sold/'
output = 'D:/Coding/real_estate_tracker/output/'
buy_main = f'{output}buy_main.csv'
sold_main = f'{output}sold_main.csv'
buy_audit = f'{output}buy_audit.txt'
sold_audit = f'{output}sold_audit.txt'

main_buy_record = ReaParser()
new_page = ReaParser()

# Backup pages:
backup_file(buy_main)
backup_file(buy_audit)


# If existing file exists, read in and store
try:
    main_buy_record.get_from_csv(buy_main, buy_audit)
except FileNotFoundError:
    main_buy_record = None

# Check if main exists. If not then do init.
# This will get the first file and then process it to start off the basics of the main file. Then it will go into the main loop below.
if main_buy_record is None:
    to_be_processed = ReaParser.get_files_in_dir(buy_pages)
    if len(to_be_processed) > 0:
        starter_file = os.path.join(buy_pages, to_be_processed[0])
        print('Starter file : ')
        print(starter_file)
        main_buy_record = ReaParser()
        main_buy_record.parse_buy_page(starter_file)
        with open(buy_main, 'w', newline='') as csvfile:
            rea_writer = csv.writer(csvfile, delimiter='|')
            rea_writer.writerow(['Address', 'Suburb', 'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Auction', 'Date updated'])
            for article in main_buy_record.articles:
                rea_writer.writerow(article.to_csv())
        with open(buy_audit, 'w', newline='') as auditfile:
            auditfile.write('[]')
        main_buy_record.set_audit(buy_audit)
        shutil.move(starter_file, os.path.join(buy_pages, 'processed', to_be_processed[0]))
        # os.rename(starter_file, starter_file.replace('.htm', '-processed.htm'))
    else:
        print('No files to process')


if main_buy_record is None:
    print('Main record is None. Exiting')
    sys.exit()
# Get all new files. Load in new file and store
to_be_processed = ReaParser.get_files_in_dir(buy_pages)
print('Files to process:')
print(to_be_processed)

# Compare new file against old records and see if there is a change. Set file to processed afterwards.
for file in to_be_processed:
    print('Processing file')
    print(file)
    file_path = buy_pages+file
    new_file = ReaParser()
    new_file.parse_buy_page(file_path)
    if len(new_file.articles) == 0:
        print('No articles from the file ' + file_path)
    main_buy_record.merge(new_file)

    shutil.move(file_path, os.path.join(buy_pages, 'processed', file.replace('.htm', '-'+str(time.mktime(datetime.now().timetuple()))+'.htm')))

with open(buy_main, 'w', newline='') as csvfile:
    rea_writer = csv.writer(csvfile, delimiter='|')
    rea_writer.writerow(['Address', 'Suburb',  'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Auction', 'Date updated'])
    for article in main_buy_record.articles:
        value = article.to_csv()
        rea_writer.writerow(value)
with open(buy_audit, 'w', newline='') as jsonaudit:
    rea_writer = csv.writer(csvfile, delimiter='|')
    json_content = json.dumps(main_buy_record.audit, sort_keys=True, indent=2)
    jsonaudit.write(json_content)




# *** Sold processing ***

# Get all pages in sold and put them into a list
# Then write out that list to the disk
# Then Load up the buy_main and see if a sold record exists for a buy. If it does, match the 2 together and save them.
# Write out the properties that sold and for what price.
'''
main_sold_record = ReaParser()
try:
    main_sold_record.get_from_csv(sold_main, sold_audit)
except:
    main_sold_record = None

if main_sold_record is None:
    main_buy_record


'''