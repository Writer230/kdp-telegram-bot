import os
from flask import Flask, request
import requests
from google import genai

app = Flask(__name__)

# 改用從環境變數讀取，這樣 GitHub 就不會報警阻擋了
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
    # 略... (保持你原本的 webhook 邏輯)
