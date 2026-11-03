import os
import time
import requests
from google import genai

# 從 Hugging Face Secrets 讀取密鑰
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 初始化 Gemini 客戶端
client = genai.Client(api_key=GEMINI_API_KEY)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def get_updates(offset=None):
    url = f"{TELEGRAM_API_URL}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return {}

def main():
    print("KDP Telegram Bot is running...")
    offset = None
    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"]["text"]
                    
                    print(f"Received message from {chat_id}: {text}")
                    
                    if text.startswith("/start"):
                        send_message(chat_id, "你好！我是你的 KDP 兒童繪本自動化助手。請直接輸入你想製作的故事主題（例如：小熊的魔法森林）。")
                    else:
                        send_message(chat_id, f"收到你的主題：「{text}」。正在呼叫 Gemini AI 為你規劃故事與內容，請稍候...")
                        
                        try:
                            # 呼叫 Gemini 生成兒童繪本大綱與內容
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=f"為兒童寫一個關於以下主題的故事，並分成 24 頁的內容與對應插圖提示詞：{text}"
                            )
                            story_result = response.text
                            send_message(chat_id, f"【故事生成完畢】\n\n{story_result[:1500]}...\n\n(系統正在為你打包 PDF 檔案...)")
                        except Exception as e:
                            send_message(chat_id, f"生成過程中發生錯誤: {str(e)}")
                            
        time.sleep(1)

if __name__ == "__main__":
    main()
