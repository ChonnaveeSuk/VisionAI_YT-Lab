import cv2
import torch
import numpy as np
import pandas as pd
import json
import yt_dlp
import os
import datetime
from ultralytics import YOLO

# กำหนดโฟลเดอร์สำหรับบันทึกไฟล์
output_webcam_dir = "C:/Vision_AI_YT/Output_Webcam"
output_ytvideo_dir = "C:/Vision_AI_YT/Output_YTvideo"
yt_info_dir = "C:/Vision_AI_YT/Youtube_Video_Info"
os.makedirs(output_webcam_dir, exist_ok=True)
os.makedirs(output_ytvideo_dir, exist_ok=True)
os.makedirs(yt_info_dir, exist_ok=True)

# โหลดโมเดล YOLOv8
model = YOLO("yolov8n.pt")

# ฟังก์ชันดาวน์โหลดวิดีโอจาก YouTube ใหม่ทุกครั้ง
def download_youtube_video(youtube_url):
    assert isinstance(youtube_url, str) and youtube_url.startswith("http"), "❌ Debug: youtube_url ไม่ถูกต้อง"
    print(f"\n✅ Debug: ดาวน์โหลดวิดีโอจากลิงก์ → {youtube_url}")

    output_path = os.path.join(output_ytvideo_dir, "youtube_video.mp4")

    # ลบไฟล์เก่าเพื่อป้องกันปัญหาคลิปซ้ำ
    if os.path.exists(output_path):
        os.remove(output_path)

    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': False,
        'noprogress': True,
        'nocheckcertificate': True,
        'retries': 3,  # ลองใหม่หากดาวน์โหลดล้มเหลว
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)

    video_title = info.get("title", "UnknownTitle").replace(" ", "_")
    channel = info.get("uploader", "UnknownChannel")
    views = info.get("view_count", 0)
    likes = info.get("like_count", 0)
    comments = info.get("comment_count", 0)

    # สร้างไฟล์ CSV และ JSON
    csv_path = os.path.join(yt_info_dir, f"{video_title}-Info.csv")
    json_path = os.path.join(yt_info_dir, f"{video_title}-Info.json")

    video_info = {
        "Title": video_title,
        "Channel": channel,
        "Views": views,
        "Likes": likes,
        "Comments": comments
    }
    
    df = pd.DataFrame([video_info])
    df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(video_info, f, indent=4)

    return output_path, video_title

# ฟังก์ชันสร้างสีไม่ซ้ำกันสำหรับ bounding box
def get_color(index):
    np.random.seed(index)
    return tuple(np.random.randint(0, 255, 3).tolist())

def detect_objects(source="webcam", save_video=False, youtube_url=None):
    """ ตรวจจับวัตถุจาก Webcam หรือ YouTube Video และบันทึกอัตโนมัติ """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if source == "webcam":
        cap = cv2.VideoCapture(0)
        output_path = os.path.join(output_webcam_dir, f"Object_detection_{timestamp}.mp4")
    elif source == "youtube":
        assert youtube_url is not None, "❌ Debug: youtube_url เป็น None"
        source, video_title = download_youtube_video(youtube_url)
        output_path = os.path.join(output_ytvideo_dir, f"{video_title}-Object_detection_{timestamp}.mp4")
        cap = cv2.VideoCapture(source)
    else:
        print("❌ Debug: แหล่งข้อมูลไม่ถูกต้อง")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480)) if save_video else None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for result in results:
            boxes = result.boxes.xyxy
            confidences = result.boxes.conf
            class_ids = result.boxes.cls

            for i, (box, conf, class_id) in enumerate(zip(boxes, confidences, class_ids)):
                x1, y1, x2, y2 = map(int, box.tolist())
                conf = round(float(conf) * 100, 1)  # แปลงเป็น %
                class_name = result.names[int(class_id)]
                label = f"{class_name} {conf}%"
                color = get_color(int(class_id))

                # วาด bounding box และแสดงชื่อวัตถุ
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        if save_video:
            out.write(frame)

        cv2.imshow("Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if save_video:
        out.release()
        print(f"\n✅ วิดีโอถูกบันทึกที่: {output_path}")

    cv2.destroyAllWindows()
