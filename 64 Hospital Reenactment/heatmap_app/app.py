import csv
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def read_csv():
    data = []
    with open('association_chart.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header row
        for row in reader:
            for value in row[:-2]:  # skip the last two columns (total_journeys, area)
                if value:  # only process non-empty cells
                    data.append(int(value))
    return data

data = read_csv()

@app.route('/')
def index():
    return render_template('heatmap.html')

@app.route('/get_data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

    



