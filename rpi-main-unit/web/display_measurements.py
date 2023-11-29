from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def show_measurements():
    # example data
    raw_measurements = [
        {'node_id': 1, 'type': 'Temperature', 'value': 22.5, 'timestamp': '2023-03-15 12:00:00'},
        {'node_id': 1, 'type': 'Humidity', 'value': 45, 'timestamp': '2023-03-15 12:05:00'},
        {'node_id': 2, 'type': 'Temperature', 'value': 23, 'timestamp': '2023-03-15 12:10:00'},
    ]
    
    measurements_by_node = {}
    for measurement in raw_measurements:
        node_id = measurement['node_id']
        if node_id not in measurements_by_node:
            measurements_by_node[node_id] = []
        measurements_by_node[node_id].append(measurement)

    return render_template('measurements.html', measurements_by_node=measurements_by_node)




if __name__ == '__main__':
    app.run(debug=True)