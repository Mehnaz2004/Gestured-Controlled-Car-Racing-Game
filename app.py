import os
import signal
import subprocess
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://Boomer:Boomer2004@cluster0.yp7ed.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.gesture_controlled_car_racing_game
gesture_collection = db.gesture_mapping  # Stores gesture bindings
process_collection = db.prototype1_process  # Stores process PID

# Function to stop any existing process
def stop_existing_process():
    """Stops the running prototype1.py process if it exists in MongoDB."""
    existing_process = process_collection.find_one({})
    if existing_process and "pid" in existing_process:
        try:
            os.kill(existing_process["pid"], signal.SIGTERM)  # Terminate process
            print(f"Stopped existing process: {existing_process['pid']}")
            process_collection.delete_one({"_id": existing_process["_id"]})  # Remove from DB
        except ProcessLookupError:
            process_collection.delete_one({"_id": existing_process["_id"]})  # Cleanup stale entry

@app.route("/")
def index():
    gesture_mappings = gesture_collection.find_one({}, {"_id": 0}) or {}

    # Normalize gesture names (convert to lowercase and remove duplicates)
    unique_gestures = {}
    for gesture, keys in gesture_mappings.items():
        normalized_gesture = gesture.lower().replace("_", " ")  # Normalize format
        if normalized_gesture not in unique_gestures:
            unique_gestures[normalized_gesture] = keys

    return render_template("index.html", gesture_mappings=unique_gestures)

@app.route("/update_mappings", methods=["POST"])
def update_mappings():
    try:
        data = request.json  # Incoming updated gesture mappings

        if data:
            for gesture, keys in data.items():
                normalized_gesture = gesture.strip().lower().title()  # Normalize name

                for hand, key in keys.items():
                    update_path = f"{normalized_gesture}.{hand}"  # Path format: "Open Palm.right"
                    gesture_collection.update_one({}, {"$set": {update_path: key}}, upsert=True)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/run_prototype", methods=["POST"])
def run_prototype():
    try:
        stop_existing_process()  # Stop any existing process

        process = subprocess.Popen(["python", "prototype1.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Store PID in MongoDB
        process_collection.insert_one({"pid": process.pid})

        return jsonify({"status": "running", "pid": process.pid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/stop_prototype", methods=["POST"])
def stop_prototype():
    """Stops the running prototype1.py process manually."""
    try:
        stop_existing_process()
        return jsonify({"status": "stopped"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/check_status", methods=["GET"])
def check_status():
    """Checks if prototype1.py is still running."""
    existing_process = process_collection.find_one({})
    if existing_process and "pid" in existing_process:
        try:
            os.kill(existing_process["pid"], 0)  # Check if process exists
            return jsonify({"status": "running", "pid": existing_process["pid"]})
        except ProcessLookupError:
            process_collection.delete_one({"_id": existing_process["_id"]})  # Cleanup stale entry
            return jsonify({"status": "not running"})
    return jsonify({"status": "not running"})

if __name__ == "__main__":
    app.run(debug=True)
