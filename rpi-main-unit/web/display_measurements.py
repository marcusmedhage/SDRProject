from flask import Flask, render_template
import sys
sys.path.insert(0, "/home/sdrgroup/Documents/SDRProject/rpi-main-unit/database")
from db_interface import get_nodes, get_measurement_latest


app = Flask(__name__)

@app.route('/')
def show_measurements():
    
    nodes = [e[0] for e in get_nodes()] # extracts all nodes in database

    measurements_by_node = {} 
    for node in nodes:
        data = get_measurement_latest(node)
        for p in data:
            if node not in measurements_by_node:
                measurements_by_node[node] = []
            measurements_by_node[node].append({'node_id': p[0], 'type': p[2], 'value': p[3], 'timestamp': p[1]})

    return render_template('measurements.html', measurements_by_node=measurements_by_node)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True)