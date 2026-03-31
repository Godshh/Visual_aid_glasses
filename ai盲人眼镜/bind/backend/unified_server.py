# backend/unified_server.py
import os
import time
import tempfile
import threading
import asyncio
import pygame
import edge_tts
import json
import re
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from http import HTTPStatus
import dashscope
from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult, Transcription
from cozepy import Coze, TokenAuth, Message, ChatEventType, COZE_CN_BASE_URL

# --- 1. 基础配置 ---
app = Flask(__name__)
CORS(app)  # 允许跨域

# 阿里云 DashScope 配置
dashscope.api_key = "sk-378eb8178dfe471b864869cccdc31b88"

# Coze 配置
COZE_PAT = "pat_loUDGE7p9lQ8kNVFv5VS3fElRBHWiX828xyEaTkv8hQI7tRjYaAZrmYzQYNwueeH"
COZE_BOT_ID = "7582114671051243520"
COZE_USER_ID = "2270947214627498"

coze = Coze(auth=TokenAuth(token=COZE_PAT), base_url=COZE_CN_BASE_URL)

# --- 2. 系统状态管理 (防回声锁) ---
class SystemState:
    def __init__(self):
        self.is_speaking = False

state = SystemState()

# --- 3. 数据清洗工具 (核心修改) ---
def clean_and_parse_response(text):
    """
    检测文本是否包含 JSON 格式的新闻/搜索结果。
    如果有，提取 title 和 summary 组合成自然语言；
    如果没有，返回原文本。
    """
    try:
        # 1. 尝试用正则提取 Markdown 代码块 ```json ... ``` 中的内容
        json_content = None
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        
        if match:
            json_content = match.group(1)
        else:
            # 2. 如果没有代码块，尝试匹配最外层的大括号 (针对裸露的 JSON)
            # 这里的正则由于要匹配嵌套结构比较复杂，简单起见匹配首尾
            stripped = text.strip()
            if stripped.startswith('{') and stripped.endswith('}'):
                json_content = stripped
        
        if json_content:
            # 尝试解析 JSON
            data = json.loads(json_content)
            
            # 构建回复：标题 + 摘要
            result_text = ""
            if 'title' in data:
                result_text += f"{data['title']}。\n"
            if 'summary' in data:
                result_text += f"{data['summary']}"
            
            # 只有当成功提取到内容时才返回清洗后的文本
            if result_text:
                print(f"🧹 已清洗 JSON 数据，转换结果: {result_text[:20]}...")
                return result_text
                
    except Exception as e:
        print(f"⚠️ JSON 解析尝试失败 (保留原文): {e}")
    
    # 如果不是 JSON 或解析失败，原样返回
    return text

# --- 4. 语音合成播报模块 (TTS) ---
async def _generate_and_play(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        temp_path = tmp_file.name
    
    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="+20%")
        await communicate.save(temp_path)
        
        if not pygame.mixer.get_init():
             pygame.mixer.init()
             
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"❌ 播报失败: {e}")
    finally:
        if os.path.exists(temp_path):
            try: os.remove(temp_path)
            except: pass

def speak_sync(text):
    if not text.strip(): return
    state.is_speaking = True
    print(f"🤖 系统正在播报: {text[:30]}...")
    try:
        asyncio.run(_generate_and_play(text))
    finally:
        time.sleep(0.5)
        state.is_speaking = False
        print("🟢 播报完成")

def recognize_audio(audio_path):
    if state.is_speaking:
        print("⚠️ 播报锁激活，忽略本次录音")
        return ""

    try:
        recognition = Recognition(
            model='paraformer-realtime-v2',
            format='wav',
            sample_rate=16000,
            callback=None
        )
        result = recognition.call(audio_path)
        if result.status_code == HTTPStatus.OK:
            text = ""
            if 'sentence' in result.output:
                for sentence in result.output['sentence']:
                    if 'text' in sentence: text += sentence['text']
            elif 'sentences' in result.output:
                for sentence in result.output['sentences']: text += sentence.get('text', '')
            
            if text:
                print(f"🗣️ 识别成功: {text}")
                return text.strip()
            return ""
        else:
            print(f"❌ ASR 错误: {result.get('message')}")
            return ""
    except Exception as e:
        print(f"❌ ASR 异常: {e}")
        return ""

# --- 5. 路由接口 ---

@app.route('/api/assistant', methods=['POST'])
def assistant():
    if 'audio' not in request.files:
        return jsonify({"error": "无音频"}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name
    
    user_text = recognize_audio(tmp_path)
    if os.path.exists(tmp_path): os.remove(tmp_path)

    if not user_text:
        status_code = 409 if state.is_speaking else 400
        return jsonify({"info": "未识别"}), status_code

    def generate_stream():
        # 1. 先发用户文字
        yield f"USER_TEXT:{user_text}\n\n"
        
        full_reply_buffer = ""
        
        try:
            # 2. 获取 Coze 完整回复 (暂存到 buffer，不直接 yield)
            stream = coze.chat.stream(
                bot_id=COZE_BOT_ID,
                user_id=COZE_USER_ID,
                additional_messages=[Message.build_user_question_text(user_text)],
            )
            
            for event in stream:
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    full_reply_buffer += event.message.content
            
            # 3. 循环结束后，统一清洗
            cleaned_text = clean_and_parse_response(full_reply_buffer)
            
            # 4. 发送清洗后的文本给前端
            # 注意：因为是一次性发送，前端会瞬间显示完，这是正常的
            yield cleaned_text
            
            # 5. 触发语音播报 (播报清洗后的文本)
            if cleaned_text:
                threading.Thread(target=speak_sync, args=(cleaned_text,), daemon=True).start()
                
        except Exception as e:
            print(f"❌ 处理异常: {e}")
            yield f"系统错误: {str(e)}"

    return Response(generate_stream(), mimetype='text/plain; charset=utf-8')

@app.route('/api/coze-text', methods=['POST', 'OPTIONS'])
def coze_text():
    if request.method == 'OPTIONS': return Response(status=200)

    data = request.get_json()
    user_text = data.get('text', '')
    print(f"💬 文字指令: {user_text}")

    def generate_text_stream():
        yield f"USER_TEXT:{user_text}\n\n"
        
        full_reply_buffer = ""
        try:
            stream = coze.chat.stream(
                bot_id=COZE_BOT_ID,
                user_id=COZE_USER_ID,
                additional_messages=[Message.build_user_question_text(user_text)],
            )
            for event in stream:
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    full_reply_buffer += event.message.content
            
            # 清洗
            cleaned_text = clean_and_parse_response(full_reply_buffer)
            
            # 返回前端
            yield cleaned_text
            
            # 播报
            if cleaned_text:
                threading.Thread(target=speak_sync, args=(cleaned_text,), daemon=True).start()
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            yield f"系统错误: {str(e)}"

    return Response(generate_text_stream(), mimetype='text/plain; charset=utf-8')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "speaking": state.is_speaking})

if __name__ == '__main__':
    pygame.mixer.init()
    print("🚀 融合版视障助手后端启动 (已启用 JSON 自动清洗)")
    print("📍 端口: 5002")
    app.run(host='0.0.0.0', port=5002, debug=True)