import csv
import os
import sys
import json
from tracker.rea_parser import ReaParser, backup_file

buy_pages = '../pages/buy/'
sold_pages = '../pages/sold/'
output = '../output/'
buy_main = f'{output}buy_main.csv'
audit = f'{output}buy_audit.txt'

main_record = ReaParser()
new_page = ReaParser()

# Backup pages:
backup_file(buy_main)
backup_file(audit)


# If existing file exists, read in and store
try:
    main_record.get_from_csv(buy_main, audit)
except FileNotFoundError:
    main_record = None

# Check if main exists. If not then do init.
if main_record is None:
    to_be_processed = ReaParser.get_files_in_dir(buy_pages)
    if len(to_be_processed) > 0:
        starter_file = os.path.join(buy_pages, to_be_processed[0])
        print('Starter file : ')
        print(starter_file)
        main_record = ReaParser()
        main_record.parse_page(starter_file)
        with open(buy_main, 'w', newline='') as csvfile:
            rea_writer = csv.writer(csvfile, delimiter='|')
            rea_writer.writerow(['Address', 'Suburb', 'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Auction', 'Date updated'])
            for article in main_record.articles:
                rea_writer.writerow(article.to_csv())
        with open(audit, 'w', newline='') as auditfile:
            auditfile.write('[]')
        main_record.set_audit(audit)
        os.rename(starter_file, starter_file.replace('.htm', '-processed.htm'))
    else:
        print('No files to process')


if main_record is None:
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
    new_file.parse_page(file_path)
    if len(new_file.articles) == 0:
        print('No articles from the file ' + file_path)
    main_record.merge(new_file)
    os.rename(file_path, file_path.replace('.htm', '-processed.htm'))

with open(buy_main, 'w', newline='') as csvfile:
    rea_writer = csv.writer(csvfile, delimiter='|')
    rea_writer.writerow(['Address', 'Suburb',  'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Auction', 'Date updated'])
    for article in main_record.articles:
        value = article.to_csv()
        rea_writer.writerow(value)
with open(audit, 'w', newline='') as jsonaudit:
    rea_writer = csv.writer(csvfile, delimiter='|')
    json_content = json.dumps(main_record.audit, sort_keys=True, indent=2)
    jsonaudit.write(json_content)


