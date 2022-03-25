import sqlite3
import csv
from rea_parser import ReaParser, Article

conn = sqlite3.connect('../db/rea.db')
conn.close()