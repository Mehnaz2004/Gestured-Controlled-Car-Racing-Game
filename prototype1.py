import cv2
import mediapipe as mp
import keyboard  # Simulating key presses

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

# Gesture to Key Mapping for both hands
GESTURE_KEY_MAPPING = {
    "Open Palm": {"right": "w", "left": "e"},  # Move Forward
    "Fist": {"right": "s", "left": "f"},  # Brake / Power-up
    "Pointing Right": {"right": "d", "left": "c"},  # Turn Right / Power-up
    "Pointing Left": {"right": "a", "left": "x"},  # Turn Left / Power-up
}

def recognize_gesture(hand_landmarks):
    """
    Recognizes a simple hand gesture based on finger positions.
    """
    landmarks = hand_landmarks.landmark

    # Get Y-coordinates of fingertips and base joints
    fingers = []
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky fingertips
    for tip in tips:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)  # Finger is up or down

    # Check for specific gestures
    index_pointing_right = fingers == [1, 0, 0, 0] and landmarks[8].x > landmarks[6].x
    index_pointing_left = fingers == [1, 0, 0, 0] and landmarks[8].x < landmarks[6].x

    if fingers == [1, 1, 1, 1]:  # All fingers up
        return "Open Palm"
    elif fingers == [0, 0, 0, 0]:  # All fingers down
        return "Fist"
    elif index_pointing_right:  # Index finger pointing right
        return "Pointing Right"
    elif index_pointing_left:  # Index finger pointing left
        return "Pointing Left"

    return "Unknown Gesture"

# Start webcam
cap = cv2.VideoCapture(0)

active_keys = set()  # Track currently pressed keys

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for natural interaction
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    detected_keys = set()  # Keys detected from gestures

    if result.multi_hand_landmarks and result.multi_handedness:
        for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
            handedness = result.multi_handedness[i].classification[0].label.lower()  # 'Left' or 'Right'
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            gesture = recognize_gesture(hand_landmarks)
            if gesture in GESTURE_KEY_MAPPING and GESTURE_KEY_MAPPING[gesture][handedness]:
                detected_key = GESTURE_KEY_MAPPING[gesture][handedness]
                detected_keys.add(detected_key)
                cv2.putText(frame, f"{handedness.capitalize()} Hand: {gesture} -> '{detected_key.upper()}'", (10, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Handle key presses and releases
    for key in detected_keys:
        if key not in active_keys:
            keyboard.press(key)  # Press new keys

    for key in active_keys - detected_keys:
        keyboard.release(key)  # Release keys no longer detected

    active_keys = detected_keys  # Update active keys

    cv2.imshow("Hand Gesture Game Control", frame)

    if cv2.waitKey(10) & 0xFF == 27:  # Press 'ESC' to exit
        break

# Release all active keys before exiting
for key in active_keys:
    keyboard.release(key)

cap.release()
cv2.destroyAllWindows()
