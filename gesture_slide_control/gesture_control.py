import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# Gesture parameters
COOLDOWN = 1.0  # Seconds between gestures
DISTANCE_THRESHOLD = 0.1  # Normalized distance for open palm/fist
THUMB_THRESHOLD = 0.05  # Threshold for thumb extension
GESTURE_LABELS = ['None', 'Next Slide', 'Previous Slide', 'Start Presentation', 'End Presentation']

# Presenter info
PRESENTER_NAME = "rewaa"
PRESENTER_STATUS = "Presenting"

def is_finger_folded(tip, pip, wrist):
    """Check if a finger is folded (tip closer to wrist than PIP joint)."""
    tip_dist = np.sqrt((tip.x - wrist.x)**2 + (tip.y - wrist.y)**2)
    pip_dist = np.sqrt((pip.x - wrist.x)**2 + (pip.y - wrist.y)**2)
    return tip_dist < pip_dist

def detect_gesture(landmarks):
    """Detect gesture based on hand landmarks."""
    # Extract key landmarks
    wrist = landmarks[0]  # Wrist (landmark 0)
    thumb_tip = landmarks[4]  # Thumb tip
    thumb_ip = landmarks[3]  # Thumb IP joint
    index_tip = landmarks[8]  # Index finger tip
    index_pip = landmarks[6]  # Index PIP joint
    middle_tip = landmarks[12]  # Middle finger tip
    middle_pip = landmarks[10]  # Middle PIP joint
    ring_tip = landmarks[16]  # Ring finger tip
    ring_pip = landmarks[14]  # Ring PIP joint
    pinky_tip = landmarks[20]  # Pinky finger tip
    pinky_pip = landmarks[18]  # Pinky PIP joint

    # Compute distances from wrist to finger tips
    thumb_dist = np.sqrt((thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2)
    index_dist = np.sqrt((index_tip.x - wrist.x)**2 + (index_tip.y - wrist.y)**2)
    middle_dist = np.sqrt((middle_tip.x - wrist.x)**2 + (middle_tip.y - wrist.y)**2)
    ring_dist = np.sqrt((ring_tip.x - wrist.x)**2 + (ring_tip.y - wrist.y)**2)
    pinky_dist = np.sqrt((pinky_tip.x - wrist.x)**2 + (pinky_tip.y - wrist.y)**2)

    # Check finger fold status for index, middle, ring, pinky
    index_folded = is_finger_folded(index_tip, index_pip, wrist)
    middle_folded = is_finger_folded(middle_tip, middle_pip, wrist)
    ring_folded = is_finger_folded(ring_tip, ring_pip, wrist)
    pinky_folded = is_finger_folded(pinky_tip, pinky_pip, wrist)

    # Next Slide (Thumbs Up): Thumb extended upward, other fingers folded
    thumb_up = (thumb_tip.y < thumb_ip.y - THUMB_THRESHOLD and
                index_folded and middle_folded and ring_folded and pinky_folded)
    
    # Previous Slide (Thumbs Down): Thumb史 extended downward, other fingers folded
    thumb_down = (thumb_tip.y > thumb_ip.y + THUMB_THRESHOLD and
                  index_folded and middle_folded and ring_folded and pinky_folded)

    # Start Presentation (Open Palm): All fingers extended
    open_palm = (thumb_dist > DISTANCE_THRESHOLD and
                 index_dist > DISTANCE_THRESHOLD and
                 middle_dist > DISTANCE_THRESHOLD and
                 ring_dist > DISTANCE_THRESHOLD and
                 pinky_dist > DISTANCE_THRESHOLD)

    # End Presentation (Closed Hand): All fingers folded
    closed_hand = (thumb_dist < DISTANCE_THRESHOLD and
                   index_dist < DISTANCE_THRESHOLD and
                   middle_dist < DISTANCE_THRESHOLD and
                   ring_dist < DISTANCE_THRESHOLD and
                   pinky_dist < DISTANCE_THRESHOLD)

    # Determine gesture
    if thumb_up:
        return 'Next Slide'
    elif thumb_down:
        return 'Previous Slide'
    elif open_palm:
        return 'Start Presentation'
    elif closed_hand:
        return 'End Presentation'
    return 'None'

def execute_action(gesture):
    """Execute slide control action based on gesture."""
    feedback = ""
    if gesture == 'Next Slide':
        pyautogui.press('right')  # Next slide
        feedback = "Next Slide ✔"
    elif gesture == 'Previous Slide':
        pyautogui.press('left')  # Previous slide
        feedback = "Previous Slide ✔"
    elif gesture == 'Start Presentation':
        pyautogui.press('f5')  # Start presentation
        feedback = "Start Presentation ✔"
    elif gesture == 'End Presentation':
        pyautogui.press('esc')  # End presentation
        feedback = "End Presentation ✔"
    return feedback

def draw_text_with_background(frame, text, position, font_scale=1, color=(0, 255, 0), thickness=2):
    """Draw text with a semi-transparent background."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x, y = position
    bg_x, bg_y = x - 5, y - text_size[1] - 5
    bg_w, bg_h = text_size[0] + 10, text_size[1] + 10

    # Draw semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (bg_x, bg_y), (bg_x + bg_w, bg_y + bg_h), (0, 0, 0), -1)
    alpha = 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Draw text
    cv2.putText(frame, text, position, font, font_scale, color, thickness)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_gesture_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        gesture = 'None'
        feedback = ""

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect gesture
                gesture = detect_gesture(hand_landmarks.landmark)

                # Execute action with cooldown
                if gesture != 'None' and (time.time() - last_gesture_time) > COOLDOWN:
                    feedback = execute_action(gesture)
                    last_gesture_time = time.time()

        # Draw presenter info
        presenter_text = f"Presenter: {PRESENTER_NAME} | Status: {PRESENTER_STATUS}"
        draw_text_with_background(frame, presenter_text, (10, 30), font_scale=0.6, color=(255, 255, 255))

        # Draw gesture feedback
        if feedback:
            draw_text_with_background(frame, feedback, (frame.shape[1]//2 - 100, frame.shape[0] - 50))
        else:
            draw_text_with_background(frame, f"Gesture: {gesture}", (frame.shape[1]//2 - 100, frame.shape[0] - 50))

        cv2.imshow('Gesture Slide Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()