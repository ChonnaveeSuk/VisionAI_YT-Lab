import os
import time
from object_detection import detect_objects
from emotion_recognition import recognize_emotions  # ✅ เพิ่มให้แน่ใจว่าเรียกใช้งาน Emotion Recognition

def main():
    print("\n🚀 Welcome to VisionAI_YT-Lab\n")
    print("🔹 เลือก Task ที่ต้องการ:")
    print("1. Emotion Recognition and Full-Body Landmark Detection")
    print("2. Object Detection (YOLOv8)")

    task_choice = input("พิมพ์หมายเลข Task ที่ต้องการ: ").strip()

    if task_choice == "1":
        print("\n✅ Debug: เริ่มต้น Emotion Recognition และ Landmark Detection...\n")
        recognize_emotions()  # ✅ เรียกใช้งาน Emotion Recognition

    elif task_choice == "2":
        print("\n📌 เลือก Input Source:")
        print("1. Webcam (Real-time Detection)")
        print("2. YouTube Video")

        input_source = input("พิมพ์หมายเลขที่ต้องการ: ").strip()
        save_video = input("\n💾 ต้องการบันทึกวิดีโอหรือไม่? (y/n): ").strip().lower() == "y"

        if input_source == "1":
            detect_objects(source="webcam", save_video=save_video)

        elif input_source == "2":
            youtube_url = input("\n🎥 กรุณาป้อนลิงก์ YouTube: ").strip()
            detect_objects(source="youtube", save_video=save_video, youtube_url=youtube_url)

        else:
            print("\n❌ Debug: เลือก Input Source ไม่ถูกต้อง!")

    else:
        print("\n❌ Debug: เลือก Task ไม่ถูกต้อง!")

if __name__ == "__main__":
    main()
