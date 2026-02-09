import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ====== CONFIG ======
BOT_TOKEN = "8561271093:AAHMXchBzSL3ag2bEWc1KpZGk80b6bIhnXk"
SHEET_NAME = "Leads"

bot = telebot.TeleBot(BOT_TOKEN)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds =creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\debas\Desktop\telegram_bot\credentials.json", scope)
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
        
        # Save to Google Sheet
        sheet.append_row([
            user_data[chat_id]["name"],
            user_data[chat_id]["phone"]
        ])
        
        bot.reply_to(message, "Thank you! Your data has been saved.")
        del user_data[chat_id]

print("Bot is running...")
bot.polling()
