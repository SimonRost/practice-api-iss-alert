import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing BOT_TOKEN or CHAT_ID in environment.")
        return

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    retries = 3

    for attempt in range(retries):
        try:
            response = requests.post(telegram_url, data=payload, timeout=5)
            response.raise_for_status()  # Raises an error for bad HTTP responses
            print("Message sent successfully.")
            return
        except Exception as e:
            print(f"Error: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Failed after retries.")
