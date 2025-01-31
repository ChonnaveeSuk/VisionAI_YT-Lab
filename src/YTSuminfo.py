import os
import csv
import json
import datetime
import telebot
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_downloader import get_video_info

# ✅ โหลด Token ของ Telegram Bot
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ ตรวจสอบโฟลเดอร์สำหรับบันทึกข้อมูล
output_dir = "C:/Vision_AI_YT/Youtube_Video_Info"
os.makedirs(output_dir, exist_ok=True)

# ✅ ฟังก์ชันดึงข้อมูล YouTube Video
def fetch_youtube_info(video_url):
    video_info = get_video_info(video_url)
    if not video_info:
        return None

    data = {
        "title": video_info["title"],
        "channel": video_info["channel"],
        "views": video_info["views"],
        "likes": video_info["likes"],
        "comments": video_info["comments"],
        "published": video_info["published"]
    }
    return data

# ✅ ฟังก์ชันส่งออก CSV
def export_csv(data, filename):
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    return file_path

# ✅ ฟังก์ชันส่งออก JSON
def export_json(data, filename):
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return file_path

# ✅ ฟังก์ชันสรุปเนื้อหาของคลิป
def summarize_youtube(video_url):
    video_id = video_url.split("v=")[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([t["text"] for t in transcript])
        summary = full_text[:300] + "..." if len(full_text) > 300 else full_text  # ตัดให้ไม่เกิน 300 ตัวอักษร
        return summary
    except Exception as e:
        return f"❌ ERROR: ไม่สามารถดึงข้อมูลจาก YouTube - {str(e)}"

# ✅ คำสั่ง `/youtubeinfo`
@bot.message_handler(commands=['youtubeinfo'])
def handle_youtubeinfo(message):
    video_url = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
    if not video_url:
        bot.reply_to(message, "❌ โปรดส่งลิงก์ YouTube")
        return

    info = fetch_youtube_info(video_url)
    if not info:
        bot.reply_to(message, "❌ ไม่สามารถดึงข้อมูลวิดีโอได้")
        return

    filename_base = f"{info['title'].replace(' ', '_')}"
    csv_path = export_csv(info, f"{filename_base}_info.csv")
    json_path = export_json(info, f"{filename_base}_info.json")

    text_response = (
        f"📺 **YouTube Video Info**\n"
        f"🔹 **Title:** {info['title']}\n"
        f"🔹 **Channel:** {info['channel']}\n"
        f"🔹 **Views:** {info['views']}\n"
        f"🔹 **Likes:** {info['likes']}\n"
        f"🔹 **Comments:** {info['comments']}\n"
        f"🔹 **Published:** {info['published']}\n"
    )

    bot.reply_to(message, text_response)
    bot.send_document(message.chat.id, open(csv_path, "rb"))
    bot.send_document(message.chat.id, open(json_path, "rb"))

# ✅ คำสั่ง `/youtubesum`
@bot.message_handler(commands=['youtubesum'])
def handle_youtubesum(message):
    video_url = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
    if not video_url:
        bot.reply_to(message, "❌ โปรดส่งลิงก์ YouTube")
        return

    summary = summarize_youtube(video_url)
    filename_base = f"youtube_summary"
    csv_path = export_csv({"video_url": video_url, "summary": summary}, f"{filename_base}.csv")

    bot.reply_to(message, f"📑 **YouTube Video Summary**\n{summary}")
    bot.send_document(message.chat.id, open(csv_path, "rb"))

# ✅ คำสั่ง `/youtubeinfosum`
@bot.message_handler(commands=['youtubeinfosum'])
def handle_youtubeinfosum(message):
    video_url = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
    if not video_url:
        bot.reply_to(message, "❌ โปรดส่งลิงก์ YouTube")
        return

    info = fetch_youtube_info(video_url)
    summary = summarize_youtube(video_url)

    if not info:
        bot.reply_to(message, "❌ ไม่สามารถดึงข้อมูลวิดีโอได้")
        return

    filename_base = f"{info['title'].replace(' ', '_')}_summary"
    csv_path = export_csv({**info, "summary": summary}, f"{filename_base}.csv")

    text_response = (
        f"📊 **YouTube Info & Summary**\n"
        f"🔹 **Title:** {info['title']}\n"
        f"🔹 **Channel:** {info['channel']}\n"
        f"🔹 **Views:** {info['views']}\n"
        f"🔹 **Likes:** {info['likes']}\n"
        f"🔹 **Comments:** {info['comments']}\n"
        f"🔹 **Published:** {info['published']}\n\n"
        f"📑 **Summary:** {summary}"
    )

    bot.reply_to(message, text_response)
    bot.send_document(message.chat.id, open(csv_path, "rb"))

# ✅ รัน Telegram Bot
bot.polling(none_stop=True)
