import os

# กำหนดโฟลเดอร์หลัก
project_root = "C:\\Vision_AI_YT"

# กำหนดโฟลเดอร์ย่อย
folders = [
    "src", "data", "models", "notebooks", "configs", "logs"
]

# กำหนดไฟล์ที่ต้องสร้าง
files = {
    "src/main.py": """import os

def main():
    print("🚀 Welcome to VisionAI_YT-Lab")
    
if __name__ == "__main__":
    main()
""",
    "src/youtube_downloader.py": """import yt_dlp

def get_video_info():
    url = input("🎥 กรุณาป้อนลิงก์ YouTube: ").strip()
    ydl_opts = {'quiet': True, 'skip_download': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        print(f"🔹 ชื่อวิดีโอ: {info['title']}")
        print(f"🔹 ชื่อช่อง: {info['uploader']}")
        print(f"🔹 ยอดวิว: {info['view_count']}")

    except Exception as e:
        print(f"❌ Error: {e}")
""",
    "src/emotion_recognition.py": """import cv2
import mediapipe as mp
from deepface import DeepFace

def detect_emotions(source="webcam"):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Emotion Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
""",
    "src/object_detection.py": """def detect_objects(source='webcam'):
    print("🔹 Object Detection ยังไม่ถูกพัฒนา")
""",
    "requirements.txt": "opencv-python\nmediapipe\ndeepface\nyt-dlp\n",
    "README.md": "# VisionAI_YT-Lab Project\n\nEnd-to-End Computer Vision with AI."
}

# สร้างโฟลเดอร์
for folder in folders:
    os.makedirs(os.path.join(project_root, folder), exist_ok=True)

# สร้างไฟล์
for file, content in files.items():
    with open(os.path.join(project_root, file), "w", encoding="utf-8") as f:
        f.write(content)

print("✅ โครงสร้างโปรเจคถูกสร้างขึ้นเรียบร้อยแล้วที่ C:\\Vision_AI_YT")
