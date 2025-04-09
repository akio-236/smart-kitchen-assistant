import cv2
import mediapipe as mp
import numpy as np


class GestureControl:
    def __init__(self, recipe_manager, timer_manager):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5
        )
        self.recipe_manager = recipe_manager
        self.timer_manager = timer_manager

    def detect(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Simple swipe detection
                landmarks = hand_landmarks.landmark
                if landmarks[8].x - landmarks[0].x > 0.1:  # Right swipe
                    return "swipe_right"
                elif landmarks[8].x - landmarks[0].x < -0.1:  # Left swipe
                    return "swipe_left"

        cap.release()
        return None

    def process_gesture(self, gesture):
        if gesture == "swipe_right":
            self.recipe_manager.next_step()
        elif gesture == "swipe_left":
            self.recipe_manager.previous_step()
