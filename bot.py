import os
import json
import telebot
import gspread
import threading
from flask import Flask
from oauth2client.service_account import ServiceAccountCredentials

# ==============================
# Environment Variables
# ==============================

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

if not GOOGLE_CREDENTIALS:
    raise ValueError("GOOGLE_CREDENTIALS not found in environment variables")

# ==============================
# Flask Web Server (Render sleep prevent)
# ==============================

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ==============================
# Telegram Bot Setup
# ==============================

bot = telebot.TeleBot(BOT_TOKEN)

SHEET_NAME = "Leads"   # তোমার Google Sheet এর নাম

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(GOOGLE_CREDENTIALS)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict, scope
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Please enter your name:")
    user_data[message.chat.id] = {}

@bot.message_handler(func=lambda message: message.chat.id in user_data)
def collect_data(message):
    chat_id = message.chat.id

    if "name" not in user_data[chat_id]:
        user_data[chat_id]["name"] = message.text
        bot.reply_to(message, "Enter your phone number:")
    elif "phone" not in user_data[chat_id]:
        user_data[chat_id]["phone"] = message.text

        sheet.append_row([
            user_data[chat_id]["name"],
            user_data[chat_id]["phone"]
        ])

        bot.reply_to(message, "Saved successfully ✅")
        del user_data[chat_id]

print("Bot is running...")
bot.infinity_polling()
