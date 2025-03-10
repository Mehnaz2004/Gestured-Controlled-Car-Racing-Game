import cv2
import mediapipe as mp
import numpy as np
import keyboard  # Replacing pyautogui

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Gesture to Key Mapping
GESTURE_KEY_MAPPING = {
    "Open Palm": "w",      # Move Forward
    "Fist": "s",           # Move Backward
    "Pointing Up": "space", # Jump
    "Thumbs Up": "d",      # Turn Right
}

def recognize_gesture(hand_landmarks):
    """
    Recognizes a simple hand gesture based on finger positions.
    """
    landmarks = hand_landmarks.landmark

    # Get Y-coordinates of fingertips and base joints
    fingers = []
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky fingertip indices
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # Fingertip above its base
            fingers.append(1)  # Finger is up
        else:
            fingers.append(0)  # Finger is down

    # Thumb (check if tip is to the right of base for a thumbs-up)
    thumb_up = landmarks[4].x > landmarks[3].x

    # Determine gesture based on finger states
    if fingers == [1, 1, 1, 1] and not thumb_up:
        return "Open Palm"
    elif fingers == [0, 0, 0, 0] and not thumb_up:
        return "Fist"
    elif fingers == [1, 0, 0, 0] and not thumb_up:
        return "Pointing Up"
    elif fingers == [0, 0, 0, 0] and thumb_up:
        return "Thumbs Up"

    return "Unknown Gesture"

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for natural movement
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    # Process detected hand landmarks
    gesture_text = "No Hand Detected"
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize gesture
            gesture = recognize_gesture(hand_landmarks)
            if gesture in GESTURE_KEY_MAPPING:
                key = GESTURE_KEY_MAPPING[gesture]
                keyboard.press_and_release(key)  # Simulate key press
                gesture_text = f"Gesture: {gesture} -> Pressing '{key.upper()}'"
            else:
                gesture_text = "Gesture: Unknown"

    # Display the detected gesture
    cv2.putText(frame, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Game Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
