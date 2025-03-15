from flask import Flask, render_template, request, jsonify
import json
import os
import subprocess
import signal

app = Flask(__name__)
MAPPING_FILE = "gesture_mappings.json"
PROCESS_FILE = "prototype1_process.txt"  # File to store process ID

# Load gesture mappings
def load_gesture_mappings():
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            return json.load(f)
    return {}

gesture_mappings = load_gesture_mappings()

# Predefined gestures (from the JSON file)
GESTURES = list(gesture_mappings.keys())

# Default function-gesture mappings
DEFAULT_FUNCTIONS = {
    "Accelerate": "Open Palm",
    "Brakes": "Fist",
    "Left": "Open Palm Tilted Left",
    "Right": "Open Palm Tilted Right"
}

# Function key bindings for both hands
KEY_BINDINGS = {
    "Accelerate": {"right": "w", "left": "e"},
    "Brakes": {"right": "s", "left": "f"},
    "Left": {"right": "d", "left": "x"},
    "Right": {"right": "a", "left": "c"}
}

def update_gesture_mappings(new_mappings):
    with open(MAPPING_FILE, "w") as f:
        json.dump(new_mappings, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html", gestures=GESTURES, functions=DEFAULT_FUNCTIONS)

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    for function, selected_gesture in data.items():
        if selected_gesture in gesture_mappings:
            # Update only existing key bindings
            gesture_mappings[selected_gesture]["right"] = KEY_BINDINGS[function]["right"]
            gesture_mappings[selected_gesture]["left"] = KEY_BINDINGS[function]["left"]

    update_gesture_mappings(gesture_mappings)
    return jsonify({"status": "success"})

# Stop any running prototype1.py before restarting
def stop_existing_process():
    if os.path.exists(PROCESS_FILE):
        with open(PROCESS_FILE, "r") as f:
            pid = f.read().strip()
        
        if pid:
            try:
                os.kill(int(pid), signal.SIGTERM)  # Terminate process
                print(f"Stopped existing process: {pid}")
            except ProcessLookupError:
                print("No running process found with PID:", pid)
            except ValueError:
                print("Invalid PID format in file")
        
        os.remove(PROCESS_FILE)  # Remove file after stopping process

@app.route("/run", methods=["POST"])
def run():
    try:
        stop_existing_process()  # Stop any existing process before running again
        process = subprocess.Popen(["python", "prototype1.py"])

        # Save new process ID
        with open(PROCESS_FILE, "w") as f:
            f.write(str(process.pid))

        return jsonify({"status": "running"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/exit", methods=["POST"])
def exit():
    if os.path.exists(PROCESS_FILE):
        stop_existing_process()  # Stop without restarting
        return jsonify({"status": "stopped"})
    else:
        return jsonify({"status": "error", "message": "No process is currently running."})

if __name__ == "__main__":
    app.run(debug=True)
