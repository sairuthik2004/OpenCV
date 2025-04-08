import cv2
import mediapipe as mp
import keyboard

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.95,
    min_tracking_confidence=0.95
)
mp_draw = mp.solutions.drawing_utils

# Landmarks
WRIST = 0
THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP = 4, 8, 12, 16, 20
INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP = 6, 10, 14, 18

# Gesture map
GESTURES = {
    "open_palm": ("Accelerate", "up"),
    "fist": ("Brake", "down"),
    "point_right": ("Turn Right", "right"),
    "point_left": ("Turn Left", "left"),
    "two_fingers_up": ("Fire Weapon", "space")
}

def is_finger_up(tip, pip, lm):
    return lm[tip].y < lm[pip].y

def classify_gesture(lm):
    fingers = {
        "thumb": lm[THUMB_TIP].x < lm[THUMB_TIP - 2].x,
        "index": is_finger_up(INDEX_TIP, INDEX_PIP, lm),
        "middle": is_finger_up(MIDDLE_TIP, MIDDLE_PIP, lm),
        "ring": is_finger_up(RING_TIP, RING_PIP, lm),
        "pinky": is_finger_up(PINKY_TIP, PINKY_PIP, lm)
    }

    # ✋ Open Palm: all fingers up
    if all(fingers.values()):
        return "open_palm"
    # ✊ Fist: all fingers down
    elif not any(fingers.values()):
        return "fist"
    # 👉 Point Right: only index up and to the right of wrist
    elif fingers["index"] and not fingers["middle"] and lm[INDEX_TIP].x > lm[WRIST].x:
        return "point_right"
    # 👈 Point Left: only index up and to the left of wrist
    elif fingers["index"] and not fingers["middle"] and lm[INDEX_TIP].x < lm[WRIST].x:
        return "point_left"
    # ✌️ Two Fingers Up: index and middle up
    elif fingers["index"] and fingers["middle"] and not fingers["ring"] and not fingers["pinky"]:
        return "two_fingers_up"
    return None

# Webcam
cap = cv2.VideoCapture(0)
active_keys = set()
prev_gesture = None
stable_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    detected_gesture = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = classify_gesture(hand_landmarks.landmark)

            if gesture == prev_gesture:
                stable_count += 1
            else:
                stable_count = 0
            prev_gesture = gesture

            if stable_count >= 3 and gesture:
                detected_gesture = gesture

    # Action mapping
    if detected_gesture:
        gesture_text, key = GESTURES[detected_gesture]
        cv2.putText(frame, f"{gesture_text}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if key not in active_keys:
            keyboard.press(key)
            active_keys.add(key)
    else:
        for key in active_keys:
            keyboard.release(key)
        active_keys.clear()

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
