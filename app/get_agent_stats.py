import json

# Read in file
# If in glenroy then process
# If agency exists in list, then +1 to sold/notsold
# If agency does not exist, add to list, then +1 sold/unsold
# 

agency = []
a = {'name': 'Ray White Glenroy', 'sold': 0, 'unsold': 0}

def in_list(name):
    for ag in agency:
        if(ag['name'] == name):
            return True
    return False

def add(name,key):
    for ag in agency:
        if(ag['name'] == name):
            ag[key] = ag[key] + 1

print(in_list('Ray White Gslenroy'))

with open('./output/collated.csv', 'r') as f:
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
            else:
                key = 'unsold'
            
            if(in_list(agencyname) == False):
                agency.append({'name': agencyname, 'sold': 0, 'unsold': 0})
            add(agencyname,key)

            
with open('./output/sold-unsold.txt', 'w') as fwrite:
    for aa in agency:
        fwrite.write(json.dumps(aa)+'\n')
