import os
import sys
import telebot
import logging
from dotenv import load_dotenv
from object_detection import detect_objects
from emotion_recognition import recognize_emotions

# ✅ ตั้งค่าให้ Python หาไฟล์ใน `src/`
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# ✅ ปิด Warning และตั้งค่าการบันทึก Log
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.basicConfig(level=logging.INFO)

# ✅ โหลด Token
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ ERROR: Invalid TELEGRAM_BOT_TOKEN! Check .env file.")

# ✅ ตั้งค่าบอท
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ คำสั่งเริ่มต้น
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to VisionAI_YT-Lab!\n"
                          "Select a task:\n"
                          "/emotion - Emotion Recognition and Full-Body Landmark Detection\n"
                          "/object - Object Detection (YOLOv8)")

# ✅ คำสั่งเลือก Emotion Recognition
@bot.message_handler(commands=['emotion'])
def handle_emotion(message):
    bot.reply_to(message, "🎭 Select Input Source:\n"
                          "/webcam - Webcam (Real-time Detection)\n"
                          "/youtube - YouTube Video")
    bot.register_next_step_handler(message, process_emotion_source)

def process_emotion_source(message):
    if message.text.lower() == "/webcam":
        bot.reply_to(message, "🎥 Initializing Emotion Recognition with Webcam...")
        try:
            recognize_emotions(source="webcam", save_video=True)
            bot.send_message(message.chat.id, "✅ Emotion Recognition completed!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ ERROR: {str(e)}")

    elif message.text.lower() == "/youtube":
        bot.reply_to(message, "📹 Please send the YouTube link:")
        bot.register_next_step_handler(message, process_youtube_emotion)

def process_youtube_emotion(message):
    youtube_url = message.text.strip()
    if youtube_url.startswith("https://"):
        bot.send_message(message.chat.id, f"⏳ Processing YouTube Video: {youtube_url}")
        try:
            recognize_emotions(source=youtube_url, save_video=True)
            bot.send_message(message.chat.id, "✅ Emotion Recognition from YouTube completed!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ ERROR: {str(e)}")
    else:
        bot.send_message(message.chat.id, "❌ Invalid YouTube link! Please try again.")

# ✅ เริ่มต้นบอท
if __name__ == "__main__":
    logging.info("✅ Telegram Bot is running...")
    bot.polling(none_stop=True)
