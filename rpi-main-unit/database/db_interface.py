import sqlite3
import datetime

def add_measurement(node_id, unit, value, time=None):
    db = sqlite3.connect("iot_data.db")
    cur = db.cursor()
    if time == None:
        current_time = datetime.datetime.now()
        # Time in 'YYYY-MM-DD HH:MM:SS' format for use with database
        time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    command = "INSERT INTO measurements VALUES (?, ?, ?, ?);"
    cur.execute(command, (node_id, time, unit, value))

    db.commit()
    cur.close()
    db.close()

def get_measurement_latest(sql_node_id):
    db = sqlite3.connect("iot_data.db")
    cur = db.cursor()
    command = f"""
    SELECT m1.*
    FROM measurements m1
    JOIN ( SELECT type, MAX(time) AS max_time
        FROM measurements
        WHERE node_id = ?
        GROUP BY type
    ) m2 ON m1.type = m2.type AND m1.time = m2.max_time
    WHERE m1.node_id = ?"""
    #with open('/home/sdrgroup/Documents/SDRProject/rpi-main-unit/database/get_latest.sql', 'r') as sql_file:
    #   sql_script = sql_file.read()
    cur.execute(command, (sql_node_id, sql_node_id))
    values = cur.fetchall()
    
    cur.close()
    db.close()

    return values

def get_nodes():
    db = sqlite3.connect("iot_data.db")
    cur = db.cursor()
    command = f"SELECT DISTINCT node_id FROM measurements;"
    cur.execute(command)
    nodes = cur.fetchall()
    
    cur.close()
    db.close()
    return nodes