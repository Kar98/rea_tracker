import re
import csv
import glob
import sys
import json
import os
import time
import shutil
from datetime import date

class ReaParser:
    article_regexp = '<article(.*?)</article>'
    audit_path = '../output/audit.txt'

    def __init__(self):
        self.articles = []
        self.audit = None
        self.date = date.today().strftime('%d/%m/%Y')

    def parse_page(self, path):
        """Parses saved html into list of articles"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if content == '':
            raise RuntimeError('File not found')

        matches = re.findall('<article(.*?)</article>', content)
        for match in matches:
            if 'Card__Box' in match and 'residential-card' in match:
                try:
                    self.articles.append(Article().parse_article(match))
                except IndexError:
                    print('Error parsing article.')
                    print(match)

        return self.articles

    def get_from_csv(self, path_to_csv, load_audit_file=''):
        with open(path_to_csv, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'Address|Suburb' not in line:
                    splits = line.split('|')
                    self.articles.append(Article(splits[0], splits[1], splits[2], splits[3], splits[4], splits[5], splits[6].replace('\n','')))
        if load_audit_file != '':
            self.set_audit(load_audit_file)
        return self.articles

    def set_audit(self, audit_path):
        with open(audit_path, 'r') as file:
            content = file.read()
        self.audit = json.loads(content)

    def merge(self, parser_to_merge):
        if self.audit is None:
            raise RuntimeError('No audit record set during merge')
        for merge_article in parser_to_merge.articles:
            found = False
            for main_article in self.articles:
                if main_article.address == merge_article.address and main_article.suburb == merge_article.suburb:
                    found = True
                    if main_article.price != merge_article.price:
                        # if audit record already exists, then add to audit and update main with latest price version
                        key_name = f'{main_article.address},{main_article.suburb}'
                        check_record = self.__is_audit(key_name)
                        print(f'Difference detected for {key_name} ')
                        print(f'Old price {main_article.price} . New price {merge_article.price}')
                        if check_record is not None:
                            # Edit
                            self.__edit_audit(key_name, merge_article.price)
                        else:
                            # Append
                            self.audit.append({'Address': key_name, 'Prices': [main_article.price , merge_article.price]})
            if not found:
                print(f'New listing : {merge_article.address},{merge_article.suburb}')
                self.articles.append(merge_article)

    def __is_audit(self, name):
        for a in self.audit:
            if a['Address'] == name:
                return a
        return None

    def __edit_audit(self, name, price):
        for a in self.audit:
            if a['Address'] == name:
                a['Prices'].append(price)

    def __edit_article(self, existing_article, new_article):
        found_article = None
        for article in self.articles:
            if article.address == existing_article.address and article.suburb == existing_article.suburb:
                found_article = article
                break
        self.articles.remove(found_article)
        self.articles.append(new_article)
        if found_article == None:
            raise RuntimeError(f'No article found for {existing_article.address},{existing_article.suburb}')

    @staticmethod
    def get_files_in_dir(folder):
        files = os.listdir(folder)
        tmplist = []
        for f in files:
            if 'processed' not in f:
                tmplist.append(f)
        return tmplist


class Article:
    def __init__(self, *args):
        try:
            self.address = args[0]
            self.suburb = args[1]
            self.price = args[2]
            self.bedrooms = args[3]
            self.bathrooms = args[4]
            self.landsize = args[5]
            self.auction = args[6]
            self.date_updated = date.today().strftime('%d/%m/%Y')
        except IndexError:
            self.address = ''
            self.suburb = ''
            self.price = ''
            self.bedrooms = ''
            self.bathrooms = ''
            self.landsize = ''
            self.auction = ''
            self.date_update = ''

    def __str__(self):
        return f' {self.address} {self.price} {self.bedrooms}/{self.bathrooms} . Size: {self.landsize} Auction: {self.auction}'

    def to_csv(self):
        return [self.address,self.suburb, self.price,self.bedrooms,self.bathrooms,self.landsize,self.auction,self.date_updated]

    def parse_article(self, content):
        x_address = 'card__details-link"><span class="">(.*?)<'
        x_agent = 'agent__name.*>(.*?)<'
        x_price = 'property-price ">(.*?)<'
        x_bedrooms = 'general-features__beds">.*?(\d+?)<'
        x_bathrooms = 'general-features__baths">.*?(\d+?)<'
        x_landsize = 'property-size__land.*?(\d+)<?'
        x_auction = 'AuctionDetails.*<span role="text">(.*?)<'

        full_address = self.__get_value(content, x_address)
        if full_address.count(',') > 1:
            tmp1, tmp2 = self.__split_multi_comma(full_address)
            self.address = tmp1
            self.suburb = tmp2.strip()
        else:
            self.address = full_address.split(',')[0]
            self.suburb = full_address.split(',')[1].strip()
        self.agent = self.__get_value(content, x_agent)
        self.price = self.__get_value(content, x_price)
        self.bedrooms = self.__get_value(content, x_bedrooms)
        self.bathrooms = self.__get_value(content, x_bathrooms)
        self.landsize = self.__get_value(content, x_landsize)
        self.auction = self.__get_value(content, x_auction)

        return self

    def __split_multi_comma(self, stringval: str):
        str1 = ''
        str2 = ''
        rindex = stringval.rindex(',')
        for i in range(0,rindex):
            str1 += stringval[i]
        for i in range(rindex+1,len(stringval)):
            str2 += stringval[i]
        return str1, str2

    def __get_value(self, content, regexp):
        try:
            return re.search(regexp, content).group(1).replace('|', '')
        except AttributeError:
            return ''


def backup_file(file_path):
    filename = os.path.basename(file_path)
    if not os.path.exists(f'{file_path}/backups'):
        os.makedirs(f'{file_path}/backups')
    # If main has been created, then create backup
    if os.path.exists(file_path):
        original_backup_filepath = f'{file_path}/backups/{filename}'
        if os.path.exists(original_backup_filepath):
            os.rename(original_backup_filepath, original_backup_filepath.replace('.csv','-'+str(int(time.now()))+'.csv'))
            shutil.copy(file_path, original_backup_filepath)

    # Replace with new one
