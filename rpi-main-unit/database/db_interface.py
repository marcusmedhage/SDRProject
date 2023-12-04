import sqlite3
import datetime

def add_measurement(node_id, time, unit, value):
    db = sqlite3.connect("iot_data.db")
    cur = db.cursor()
    current_time = datetime.now()
    # Time in 'YYYY-MM-DD HH:MM:SS' format for use with database
    time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    command = f"INSERT INTO measurements ({node_id}, {time}, {unit}, {value});"
    cur.execute(command)

    db.commit()
    cur.close()
    db.close()

def get_measurement_latest(node_id):
    db = sqlite3.connect("iot_data.db")
    cur = db.cursor()
    with open('get_latest.sql', 'r') as sql_file:
       sql_script = sql_file.read()
    cur = db.cursor()
    cur.executescript(sql_script)
    
    db.commit()
    cur.close()
    db.close