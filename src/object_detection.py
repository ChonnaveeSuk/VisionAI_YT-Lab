import cv2
import os
import datetime
import random
from telebot import TeleBot
from dotenv import load_dotenv
from youtube_downloader import download_youtube_video  # ✅ ใช้สำหรับดาวน์โหลดวิดีโอ YouTube
from ultralytics import YOLO  # ✅ ใช้ YOLOv8 โดยตรง

# ✅ โหลด Token ของ Telegram Bot
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ ตรวจสอบโฟลเดอร์สำหรับบันทึกวิดีโอ
output_dir = "C:/Vision_AI_YT/Output_Processed"
os.makedirs(output_dir, exist_ok=True)

# ✅ โหลดโมเดล YOLOv8 Nano Model
model_path = "C:/Vision_AI_YT/yolov8n.pt"
model = YOLO(model_path)

# ✅ ฟังก์ชันสุ่มสีให้ Bounding Box แต่ละวัตถุ
def get_random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))  # ✅ สีที่อ่านง่าย

# ✅ ฟังก์ชันตรวจจับวัตถุ (รองรับ YouTube และ Webcam)
def recognize_objects(source="webcam", save_video=False, youtube_url=None, chat_id=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(output_dir, f"Object_Detection_{timestamp}.mp4")

    if source == "youtube":
        video_path = download_youtube_video(youtube_url)  # ✅ ดาวน์โหลดวิดีโอ YouTube
        cap = cv2.VideoCapture(video_path)
    else:
        cap = cv2.VideoCapture(0)  # ✅ ใช้ Webcam

    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height)) if save_video else None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)  # ✅ รันโมเดล YOLOv8 บนเฟรม

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # ✅ ค่าตำแหน่ง Bounding Box
                conf = box.conf[0].item()  # ✅ ความมั่นใจ
                cls = int(box.cls[0].item())  # ✅ ประเภทของวัตถุ
                label = f"{model.names[cls]} {conf:.2f}"  # ✅ ชื่อวัตถุ + ความมั่นใจ
                color = get_random_color()

                # ✅ วาด Bounding Box และ Label บนภาพ
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        if save_video:
            out.write(frame)

        cv2.imshow("YOLOv8 Object Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == ord("Q"):
            print("\n✅ Exporting Video...")
            cap.release()
            if save_video:
                out.release()
                bot.send_message(chat_id, "✅ Exported Processed Video!")
                with open(output_path, "rb") as video:
                    bot.send_video(chat_id, video)
            break

    cv2.destroyAllWindows()
