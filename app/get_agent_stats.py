import json
from tracker.rea_parser import ReaParser
# Read in file
# If in glenroy then process
# If agency exists in list, then +1 to sold/notsold
# If agency does not exist, add to list, then +1 sold/unsold
# 

agencies = []
parser = ReaParser()
a = {'name': 'example', 'sold': 0, 'unsold': 0}

def in_list(name):
    for ag in agencies:
        if(ag['name'] == name):
            return True
    return False

def add(name,kkey):
    for ag in agencies:
        if(ag['name'] == name):
            ag[kkey] = ag[kkey] + 1
            return

parser.get_from_csv('./output/sold_main.txt')
for article in parser.articles:
    if article.suburb == 'Glenroy':
        if(in_list(article.agency) == False):
            agencies.append({'name': article.agency, 'sold': 0, 'unsold': 0})
        if(article.sold == '1'):
            kkey = 'sold'
        elif (article.sold == '0'):
            kkey = 'unsold'
        else:
            kkey = ''
        if(in_list(article.agency) == False):
            agencies.append({'name': article.agency, 'sold': 0, 'unsold': 0})
        if kkey != '':
            add(article.agency,kkey)

"""
with open('./output/sold_main.txt', 'r') as f:
    lines = f.readlines()
    for r in range(1,len(lines)):
        line = lines[r]
        splits = line.split('|')
        suburb = splits[1]
        agencyname = splits[3]
        sold = splits[6]
        if(suburb == 'Glenroy'):
            if(sold == '1\n'):
                key = 'sold'
            elif (sold == '0\n'):
                key = 'unsold'
            
            if(in_list(agencyname) == False):
                agency.append({'name': agencyname, 'sold': 0, 'unsold': 0})
            if(key == 'sold' or key == 'unsold'):
                add(agencyname,key)
"""

def get_sold(record):
    return record.get('sold')

agencies.sort(key=get_sold, reverse=True)
print(agencies)

with open('./output/sold-unsold.txt', 'w') as fwrite:
    for aa in agencies:
        fwrite.write(json.dumps(aa)+'\n')
