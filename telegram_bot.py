import telebot
import os
import sys
import logging
from dotenv import load_dotenv

# ✅ ตั้งค่า Debug Logging
logging.basicConfig(level=logging.DEBUG)

# ✅ ใช้ Path เต็ม แทน `os.path.join`
SRC_DIR = "C:/Vision_AI_YT/src"
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# ✅ Debug ตรวจสอบว่า Python มองเห็น `src/` หรือไม่
print(f"✅ Debug: SRC_DIR = {SRC_DIR}")
print(f"✅ Debug: Current sys.path = {sys.path}")

# ✅ Import โมดูลหลังจากเพิ่ม Path แล้ว (แก้ปัญหา ImportError)
try:
    from object_detection import recognize_objects
    from emotion_recognition import recognize_emotions
    from youtube_downloader import get_video_info, download_youtube_video
except ModuleNotFoundError as e:
    print(f"❌ ERROR: {e}")
    print("🔹 ตรวจสอบว่าไฟล์ `object_detection.py` และ `emotion_recognition.py` อยู่ใน `C:/Vision_AI_YT/src/` หรือไม่")
    sys.exit(1)

# ✅ โหลดค่า TOKEN จาก .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ ตรวจสอบว่า Token ถูกต้อง
if not TELEGRAM_BOT_TOKEN or ":" not in TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN ไม่ถูกต้อง! โปรดตรวจสอบ .env")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ เก็บ Task ที่ผู้ใช้เลือก (emotion หรือ object)
selected_task = {}

# ✅ คำสั่งเริ่มต้น
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to VisionAI_YT-Lab!\n"
                          "Select a task:\n"
                          "/emotion - Emotion Recognition and Full-Body Landmark Detection\n"
                          "/object - Object Detection (YOLOv8)")

# ✅ คำสั่งสำหรับ Emotion Recognition
@bot.message_handler(commands=['emotion'])
def handle_emotion(message):
    selected_task[message.chat.id] = "emotion"
    bot.reply_to(message, "🎭 Select Input Source:\n"
                          "/webcam - Webcam (Real-time Detection)\n"
                          "/youtube - YouTube Video")

# ✅ คำสั่งสำหรับ Object Detection
@bot.message_handler(commands=['object'])
def handle_object(message):
    selected_task[message.chat.id] = "object"
    bot.reply_to(message, "🔍 Select Input Source:\n"
                          "/webcam - Webcam (Real-time Detection)\n"
                          "/youtube - YouTube Video")

# ✅ คำสั่งสำหรับตรวจจับจาก Webcam
@bot.message_handler(commands=['webcam'])
def handle_webcam(message):
    if selected_task.get(message.chat.id) == "emotion":
        bot.reply_to(message, "🎭 Initializing Emotion Recognition with Webcam...")
        recognize_emotions(source="webcam", save_video=True, chat_id=message.chat.id)
    elif selected_task.get(message.chat.id) == "object":
        bot.reply_to(message, "🔍 Initializing Object Detection with Webcam...")
        recognize_objects(source="webcam", save_video=True, chat_id=message.chat.id)
    else:
        bot.reply_to(message, "❌ ERROR: Please select /emotion or /object first!")

# ✅ คำสั่งสำหรับตรวจจับจาก YouTube
@bot.message_handler(commands=['youtube'])
def handle_youtube(message):
    bot.reply_to(message, "📹 Please send the YouTube link:")
    bot.register_next_step_handler(message, process_youtube_link)

def process_youtube_link(message):
    youtube_link = message.text.strip()
    if youtube_link.startswith("https://www.youtube.com/") or youtube_link.startswith("https://youtu.be/"):
        bot.send_message(message.chat.id, f"⏳ Processing YouTube Video:\n{youtube_link}")

        # ✅ ตรวจสอบว่าผู้ใช้เลือก /emotion หรือ /object ก่อนเรียกใช้ฟังก์ชันที่ถูกต้อง
        if selected_task.get(message.chat.id) == "emotion":
            recognize_emotions(source="youtube", youtube_url=youtube_link, save_video=True, chat_id=message.chat.id)
        elif selected_task.get(message.chat.id) == "object":
            recognize_objects(source="youtube", youtube_url=youtube_link, save_video=True, chat_id=message.chat.id)
        else:
            bot.send_message(message.chat.id, "❌ ERROR: Please select /emotion or /object first!")
    else:
        bot.send_message(message.chat.id, "❌ Please send a valid YouTube link!")

# ✅ เริ่มต้น Bot
bot.polling(none_stop=True)
