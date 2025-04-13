import sqlite3
import re
# Connecting to the database
conn = sqlite3.connect('wikipedia_pages.db')

# Creating a cursor object so we can execute commads
curs = conn.cursor()

# Example INSERT line from dump
line = "INSERT INTO `pagelinks` VALUES (123,0,456),(124,0,457),(125,0,458);"

# Regex: capture only the first and third values in each tuple
matches = re.findall(r'\((\d+),\d+,(\d+)\)', line)

print(matches)

