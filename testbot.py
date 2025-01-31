import telebot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
print(bot.get_me())  # ✅ ตรวจสอบว่า Bot ออนไลน์
