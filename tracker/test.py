import re
import csv
import glob
import json
import os
from datetime import date
import time

str1 = '5,6,7/1100 Sydney Road, Fawkner'

val1 = 'E:/Coding/real_estate_tracker/pages/buy/glenroy1-processed.htm'
num = 1648167365.4417772

my_time = time.strftime('%Y-%m-%d', time.localtime(num))

ret1 = os.path.getatime(val1)
ret2 = os.path.getmtime(val1)
ret3 = os.path.getctime(val1)

print(my_time)



