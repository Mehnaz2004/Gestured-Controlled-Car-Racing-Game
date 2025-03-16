from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import subprocess

app = Flask(__name__)

# Establish MongoDB connection
client = MongoClient('mongodb+srv://Boomer:Boomer2004@cluster0.yp7ed.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['gesture_controlled_car_racing_game']
gesture_collection = db['gesture_mapping']

# Store the process reference
process = None

@app.route('/')
def landing_page():
    document = gesture_collection.find_one()
    if document:
        gesture_mappings = {k: v for k, v in document.items() if k != '_id'}
    else:
        gesture_mappings = {}
    return render_template('index.html', gesture_mappings=gesture_mappings)

@app.route('/update_mappings', methods=['POST'])
def update_mappings():
    data = request.json
    if data:
        gesture_collection.update_one({}, {'$set': data}, upsert=True)
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/run_prototype', methods=['POST'])
def run_prototype():
    global process
    if process is not None:
        process.terminate()
        process = None
    try:
        process = subprocess.Popen(['python', 'prototype1.py'])
        return jsonify({'status': 'running'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stop_prototype', methods=['POST'])
def stop_prototype():
    global process
    if process is not None:
        process.terminate()
        process = None
        return jsonify({'status': 'stopped'}), 200
    return jsonify({'status': 'error', 'message': 'No process running'}), 400

if __name__ == '__main__':
    app.run(debug=True)
