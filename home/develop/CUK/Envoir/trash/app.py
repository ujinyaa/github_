

'''
from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/data')
def data():
    json_path = os.path.join(os.path.dirname(__file__), 'processed_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
'''
'''