import cv2
import mediapipe as mp
import keyboard  # For simulating key presses
import sys
from pymongo import MongoClient

if len(sys.argv) != 2:
    print("User email argument missing.")
    sys.exit(1)

user_email = sys.argv[1]

def load_gesture_mappings():
    """Loads the gesture-key mappings from MongoDB for the current user."""
    client = MongoClient("mongodb+srv://Boomer:Boomer2004@cluster0.yp7ed.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.gesture_controlled_car_racing_game
    collection = db.user_profile

    user_data = collection.find_one({"email": user_email})
    if user_data and "gesture_mappings" in user_data:
        return user_data["gesture_mappings"]
    else:
        print("No gesture mapping found for the user!")
        return {}

# Gesture to Key Mapping
GESTURE_KEY_MAPPING = load_gesture_mappings()

# Track the active key for each hand
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

active_keys = {"right": None, "left": None}

def recognize_gesture(hand_landmarks):
    """
    Recognizes a hand gesture based on finger positions.
    """
    landmarks = hand_landmarks.landmark

    fingers = []
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky fingertip indices
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # Fingertip above its base
            fingers.append(1)  # Finger is up
        else:
            fingers.append(0)  # Finger is down

    # Hand tilt detection using wrist and finger base positions
    wrist_x = landmarks[0].x
    middle_base_x = landmarks[9].x  # Base of middle finger
    tilt_threshold = 0.05  # Minimum required tilt to classify as tilted

    # Gesture Conditions
    if fingers == [1, 1, 0, 0]:
        return "Victory"
    elif fingers == [1, 1, 1, 0]:
        return "Three Fingers Up"
    elif fingers == [1, 1, 1, 1]:
        # Detect significant left or right tilt
        if wrist_x < middle_base_x - tilt_threshold:
            return "Open Palm Tilted Left"  # Palm tilted left
        elif wrist_x > middle_base_x + tilt_threshold:
            return "Open Palm Tilted Right"  # Palm tilted right
        return "Open Palm"
    elif fingers == [0, 0, 0, 0]:
        return "Fist"

    return None  # No recognized gesture

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    detected_keys = {"right": None, "left": None}

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness_info in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            handedness = "left" if handedness_info.classification[0].label.lower() == "left" else "right"
            gesture = recognize_gesture(hand_landmarks)

            if gesture and gesture in GESTURE_KEY_MAPPING:
                detected_keys[handedness] = GESTURE_KEY_MAPPING[gesture][handedness]

    # Handle key presses and releases using your logic
    for hand in ["right", "left"]:
        detected_key = detected_keys[hand]
        active_key = active_keys[hand]

        if detected_key and detected_key != active_key:
            if active_key:
                keyboard.release(active_key)  # Release previous key
            keyboard.press(detected_key)  # Hold new key
            active_keys[hand] = detected_key

        elif not detected_key and active_key:
            keyboard.release(active_key)  # Release the key if no valid gesture
            active_keys[hand] = None

    # Display gesture information
    for i, (hand, key) in enumerate(detected_keys.items()):
        text = f"{hand.capitalize()} Hand: {'Holding ' + key.upper() if key else 'No Gesture'}"
        cv2.putText(frame, text, (10, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Game Control", frame)

    if cv2.waitKey(10) & 0xFF == 27:  # Press 'ESC' to exit
        break

# Release any active keys before exiting
for key in active_keys.values():
    if key:
        keyboard.release(key)

cap.release()
cv2.destroyAllWindows()
