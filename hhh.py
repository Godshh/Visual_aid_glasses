# local_viewer_with_ai.py —— 纯本地看 + 手势特效（不发回去，延迟≈0）
import asyncio
import websockets
import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from datetime import datetime

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
WS_URL = "ws://121.43.195.181:5001/ws/cam/"   # 你的服务器地址
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,                 # 这里可以开满！本地无压力
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

danmu_queue = deque(maxlen=12)

async def local_only_viewer():
    async with websockets.connect(WS_URL, max_size=None) as ws:
        print(f"已连接到服务器 → {WS_URL}")
        print("现在只有你自己能看到超精准手势特效！（其他人看不到）")
        print("按 q 退出窗口")

        while True:
            try:
                msg = await ws.recv()

                # 弹幕
                if isinstance(msg, str):
                    try:
                        data = eval(msg) if msg.startswith("{") else {}
                        if data.get("cmd") == "bullet":
                            ts = datetime.now().strftime("%H:%M")
                            danmu_queue.append(f"{ts} {data.get('text','')[:30]}")
                    except: pass
                    continue

                # 视频帧
                if isinstance(msg, bytes):
                    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), cv2.IMREAD_COLOR)
                    if frame is None: continue

                    h, w = frame.shape[:2]
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb)

                    # 手势识别 + 超炫特效（本地随便浪）
                    if results.multi_hand_landmarks:
                        for hand_lm in results.multi_hand_landmarks:
                            mp_draw.draw_landmarks(
                                frame, hand_lm, mp_hands.HAND_CONNECTIONS,
                                mp_draw.DrawingSpec(color=(0,255,255), thickness=3, circle_radius=4),
                                mp_draw.DrawingSpec(color=(255,0,255), thickness=3)
                            )
                            # 精准握拳
                            wrist_y = hand_lm.landmark[0].y
                            tips = [hand_lm.landmark[i].y for i in [8,12,16,20]]
                            if all(t > wrist_y + 0.08 for t in tips):
                                cv2.putText(frame, "GRAB!!!", (w//2-300, h//2+80),
                                            cv2.FONT_HERSHEY_DUPLEX, 8, (0,0,255), 20)
                                cv2.rectangle(frame, (0,0), (w,h), (0,0,255), 40)
                                # 可以再加个爆炸特效、音效、贴纸啥的……

                    # 画弹幕
                    overlay = frame.copy()
                    for i, text in enumerate(danmu_queue):
                        y = 100 + i * 70
                        cv2.putText(overlay, text, (50, y),
                                    cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,0), 5, cv2.LINE_AA)
                        cv2.rectangle(overlay, (40, y-70), (w-40, y+20), (0,0,0), -1)
                    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

                    # 本地显示（超清超快）
                    cv2.imshow("【本地专属】手势识别 + 弹幕（只有你看得到）", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            except Exception as e:
                print(f"断开或异常：{e}")
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("="*80)
    print("纯本地手势特效查看器启动成功！")
    print("服务器只是转发裸流，你本地随便加特效、YOLO、贴纸、虚拟背景……")
    print("其他人完全看不到你的特效 → 真正的“开挂”模式！")
    print("="*80)
    asyncio.run(local_only_viewer())