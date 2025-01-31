import os
import sys
import logging
import torch

# ✅ ตั้งค่า Debug Logging
logging.basicConfig(level=logging.DEBUG)

# ✅ ใช้ Path เต็ม แทน `os.path.join`
SRC_DIR = "C:/Vision_AI_YT/src"
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# ✅ Debug ตรวจสอบว่า Python มองเห็น `src/` หรือไม่
print(f"✅ Debug: SRC_DIR = {SRC_DIR}")
print(f"✅ Debug: Current sys.path = {sys.path}")

# ✅ ตรวจสอบว่าใช้ CPU หรือ GPU
if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print(f"✅ Debug: ใช้ GPU {torch.cuda.get_device_name(0)}")
else:
    DEVICE = torch.device("cpu")
    print("⚠️ Debug: ไม่พบ GPU, ใช้ CPU เท่านั้น")

# ✅ ปิด TensorFlow Delegate เพื่อเพิ่มความเร็ว
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # ลด Logging ของ TensorFlow

# ✅ Import โมดูลหลัก
try:
    print("🚀 Debug: เริ่มโหลดโมเดล Object Detection...")
    from object_detection import recognize_objects
    print("✅ Debug: โหลด Object Detection สำเร็จ!")

    print("🚀 Debug: เริ่มโหลดโมเดล Emotion Recognition...")
    from emotion_recognition import recognize_emotions
    print("✅ Debug: โหลด Emotion Recognition สำเร็จ!")
except ModuleNotFoundError as e:
    print(f"❌ ERROR: {e}")
    print("🔹 ตรวจสอบว่าไฟล์ `object_detection.py` และ `emotion_recognition.py` อยู่ใน `C:/Vision_AI_YT/src/` หรือไม่")
    sys.exit(1)

# ✅ ฟังก์ชันหลัก
def main():
    while True:
        print("\n🎬 VisionAI_YT-Lab - Main Script 🎬")
        print("1️⃣ Emotion Recognition (Webcam)")
        print("2️⃣ Emotion Recognition (YouTube)")
        print("3️⃣ Object Detection (Webcam)")
        print("4️⃣ Object Detection (YouTube)")
        print("5️⃣ Exit")

        choice = input("\n🔹 Select an option (1-5): ").strip()

        if choice == "1":
            print("🎭 Starting Emotion Recognition (Webcam)...")
            recognize_emotions(source="webcam", save_video=True)

        elif choice == "2":
            youtube_url = input("📹 Enter YouTube URL: ").strip()
            print(f"🎭 Processing YouTube Video: {youtube_url}")
            recognize_emotions(source="youtube", youtube_url=youtube_url, save_video=True)

        elif choice == "3":
            print("🔍 Starting Object Detection (Webcam)...")
            recognize_objects(source="webcam", save_video=True)

        elif choice == "4":
            youtube_url = input("📹 Enter YouTube URL: ").strip()
            print(f"🔍 Processing YouTube Video: {youtube_url}")
            recognize_objects(source="youtube", youtube_url=youtube_url, save_video=True)

        elif choice == "5":
            print("👋 Exiting...")
            sys.exit(0)

        else:
            print("❌ Invalid Option! Please try again.")

if __name__ == "__main__":
    main()
