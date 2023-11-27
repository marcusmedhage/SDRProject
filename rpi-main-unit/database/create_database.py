import sqlite3

db = sqlite3.connect("iot_data.db")
cur = db.cursor()

with open('create_database.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cur.executescript(sql_script)
db.commit()


