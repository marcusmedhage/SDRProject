import sqlite3
import datetime

db = sqlite3.connect("iot_data.db")
cur = db.cursor()

def add_measurement(node_id, unit, value):
    current_time = datetime.now()
    # Time in 'YYYY-MM-DD HH:MM:SS' format for use with database
    time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    command = f"INSERT INTO measurements ({node_id}, {time}, {unit}, {value});"
    cur.execute(command)

    db.commit()
    cur.close()
    db.close()

def get_measurement_latest(node_id, unit):
    pass