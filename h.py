# local_save_ai_frames.py —— 每帧高清保存 + 手势特效（纯本地离线神器）
import asyncio
import websockets
import cv2
import numpy as np
import mediapipe as mp
import os
from datetime import datetime
from collections import deque

# ==================== 配置区 ====================
WS_URL = "ws://121.43.195.181:5001/ws/cam/"  # 你的服务器地址
# 服务器摄像头+手势识别
# 保存路径（自动创建）
SAVE_DIR = "AI特效截图"  # 改成你喜欢的文件夹名
os.makedirs(SAVE_DIR, exist_ok=True)

# 保存模式（三选一）
SAVE_ALL_FRAMES = False  # True=每帧都保存（生成视频素材）
SAVE_ON_GRAB_ONLY = True  # True=只在检测到握拳时保存（推荐！）
SAVE_INTERVAL = 3  # 每隔几秒保存一次（防重复）
# ===============================================

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,  # 本地随便开最高精度！
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

last_save_time = 0
grab_detected = False


async def local_ai_saver():
    global last_save_time, grab_detected

    async with websockets.connect(WS_URL, max_size=None) as ws:
        print(f"已连接服务器 → {WS_URL}")
        print(f"所有特效帧将保存到：{os.path.abspath(SAVE_DIR)}")
        print("检测到握拳会自动保存高清特效图！按 q 退出")

        frame_count = 0
        while True:
            try:
                msg = await ws.recv()

                if isinstance(msg, bytes):
                    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), cv2.IMREAD_COLOR)
                    if frame is None: continue

                    frame_count += 1
                    h, w = frame.shape[:2]
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb)

                    # 重置握拳状态
                    grab_detected = False

                    if results.multi_hand_landmarks:
                        for hand_lm in results.multi_hand_landmarks:
                            mp_draw.draw_landmarks(
                                frame, hand_lm, mp_hands.HAND_CONNECTIONS,
                                mp_draw.DrawingSpec(color=(0, 255, 255), thickness=4),
                                mp_draw.DrawingSpec(color=(255, 0, 255), thickness=4)
                            )
                            # 超精准握拳检测
                            wrist_y = hand_lm.landmark[0].y
                            tips = [hand_lm.landmark[i].y for i in [8, 12, 16, 20]]
                            if all(t > wrist_y + 0.08 for t in tips):
                                grab_detected = True
                                cv2.putText(frame, "GRAB!!!", (w // 2 - 350, h // 2 + 100),
                                            cv2.FONT_HERSHEY_DUPLEX, 10, (0, 0, 255), 25)
                                cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 255), 50)
                                cv2.putText(frame, "SAVED!", (w // 2 - 200, h - 100),
                                            cv2.FONT_HERSHEY_DUPLEX, 4, (0, 255, 0), 10)

                    # ==================== 保存逻辑 ====================
                    now = datetime.now()
                    should_save = False

                    if SAVE_ALL_FRAMES:
                        should_save = True
                    elif SAVE_ON_GRAB_ONLY and grab_detected:
                        should_save = True
                    elif (now.timestamp() - last_save_time) > SAVE_INTERVAL:
                        should_save = True

                    if should_save:
                        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]
                        reason = "grab" if grab_detected else "timer" if (
                                                                                     now.timestamp() - last_save_time) > SAVE_INTERVAL else "all"
                        filename = f"{SAVE_DIR}/{timestamp}_{reason}_frame{frame_count:06d}.jpg"

                        # 保存超高清原图（质量100！）
                        cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(filename)
                        print(f"已保存 → {filename}")
                        last_save_time = now.timestamp()

                    # 本地预览
                    cv2.imshow("本地AI特效预览（高清保存中）", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            except Exception as e:
                print(f"断开：{e}")
                break

    cv2.destroyAllWindows()
    print(f"程序结束，共保存 {frame_count} 帧到 {SAVE_DIR}")


if __name__ == "__main__":
    print("=" * 80)
    print("本地AI特效高清保存神器启动！")
    print("功能：手势识别 + 握拳自动截图 + 定时保存 + 最高画质输出")
    print("=" * 80)
    asyncio.run(local_ai_saver())