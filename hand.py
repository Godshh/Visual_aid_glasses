import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

def is_grab_gesture(landmarks):
    # 简单抓取判断：检查手指尖与掌心距离（自定义阈值）
    if len(landmarks) == 0:
        return False
    # 示例：检查食指尖 (tip=8) 与腕部 (wrist=0) 弯曲
    wrist = np.array([landmarks[0].x, landmarks[0].y])
    tip = np.array([landmarks[8].x, landmarks[8].y])
    distance = np.linalg.norm(tip - wrist)
    return distance < 0.05  # 阈值调整，根据测试

while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if is_grab_gesture(hand_landmarks.landmark):
                cv2.putText(frame, 'Grab Intention Detected!', (50, 50), cv2.FONT_HERSY_SIMPLE, 1, (0, 255, 0), 2)
    cv2.imshow('Hand Landmark', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()