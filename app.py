from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import subprocess
import bcrypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Establish MongoDB connection
client = MongoClient('mongodb+srv://Boomer:Boomer2004@cluster0.yp7ed.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['gesture_controlled_car_racing_game']
gesture_collection = db['gesture_mapping']
user_collection = db['user_profile']

# Default gesture mappings
default_mappings = {
    "Open Palm": {"right": "w", "left": "e"},
    "Fist": {"right": "s", "left": "f"},
    "Open Palm Tilted Left": {"right": "c", "left": "d"},
    "Open Palm Tilted Right": {"right": "x", "left": "a"},
    "Victory": {"right": "v", "left": "b"},
    "Three Fingers Up": {"right": "h", "left": "n"}
}

# Store the process reference
process = None

@app.route('/')
def landing_page():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user_data = user_collection.find_one({"email": session['user']})
        gesture_mappings = user_data.get("gesture_mappings", default_mappings)
        return render_template('index.html', gesture_mappings=gesture_mappings)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_collection.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user'] = email
            return redirect(url_for('dashboard'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if user_collection.find_one({"email": email}):
            return "User already exists", 409
        user_collection.insert_one({"email": email, "password": hashed_password, "gesture_mappings": default_mappings})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/update_mappings', methods=['POST'])
def update_mappings():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    data = request.json
    if data:
        user_collection.update_one(
            {"email": session['user']},
            {'$set': {"gesture_mappings": data}},
            upsert=True
        )
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/run_prototype', methods=['POST'])
def run_prototype():
    global process
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    if process is not None:
        process.terminate()
        process = None

    user_email = session['user']
    process = subprocess.Popen(['python', 'prototype1.py', user_email])
    return jsonify({'status': 'running'}), 200

@app.route('/stop_prototype', methods=['POST'])
def stop_prototype():
    global process
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    if process is not None:
        process.terminate()  # Try to terminate first
        process.wait()  # Wait for process to end
        process = None
        return jsonify({'status': 'stopped'}), 200
    return jsonify({'status': 'error', 'message': 'No process running'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
