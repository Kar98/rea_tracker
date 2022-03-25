import re
import csv
import glob
import json
import os
from datetime import date
import time

str1 = '5,6,7/1100 Sydney Road, Fawkner'

val1 = os.path.basename('../output/buy_main.csv')
val2 = '.csv'+str(int(time.time()))
print(val1)
print(val2)