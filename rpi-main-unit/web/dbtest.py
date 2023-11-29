import sqlite3
import os

print("Current Working Directory:", os.getcwd())

con = sqlite3.connect('chinook.db')
cur = con.cursor()

print("Test")

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
for table in tables:
    print(table[0])