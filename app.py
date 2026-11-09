import os
from flask import Flask, request
import requests
from google import genai

app = Flask(__name__)

# 安全地從 PythonAnywhere 環境變數讀取
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 初始化 Gemini 客戶端
client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        if text == "/start":
            send_telegram_message(chat_id, "你好！我是你的 KDP 兒童繪本自動化助手。請直接輸入你想製作的故事主題（例如：小熊的魔法森林）。")
        else:
            send_telegram_message(chat_id, f"收到你的主題：「{text}」。正在呼叫 Gemini AI 為你規劃故事與內容，請稍候...")
            try:
                # 呼叫 Gemini 3.8 Flash 生成故事
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"請為兒童繪本創作一個關於「{text}」的故事大綱與內容。"
                )
                story = response.text
                send_telegram_message(chat_id, story)
            except Exception as e:
                send_telegram_message(chat_id, f"生成過程中發生錯誤：{str(e)}")
                
    return "OK", 200

@app.route('/')
def index():
    return "KDP Telegram Bot is running via Webhook!", 200

if __name__ == '__main__':
    app.run()
