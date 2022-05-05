import re
import csv
import glob
import json
import os
from datetime import date, datetime
import time

str1 = '5,6,7/1100 Sydney Road, Fawkner'

val1 = '20/03/2022'
val2 = '25/03/2022'

ret1 = datetime.strptime(val1, '%d/%m/%Y')
ret2 = datetime.strptime(val2, '%d/%m/%Y')

if ret1 > ret2:
    print('ret 1 >')
else:
    print('ret 2 > ')


