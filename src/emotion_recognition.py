import cv2
import mediapipe as mp
import numpy as np
import os
import datetime

# ✅ ตรวจสอบโฟลเดอร์สำหรับบันทึกไฟล์
output_webcam_dir = "C:/Vision_AI_YT/Output_Webcam"
output_ytvideo_dir = "C:/Vision_AI_YT/Output_YTvideo"
os.makedirs(output_webcam_dir, exist_ok=True)
os.makedirs(output_ytvideo_dir, exist_ok=True)

# ✅ ฟังก์ชันหลักสำหรับ Emotion Recognition
def recognize_emotions(source="webcam", save_video=False):
    """
    ตรวจจับอารมณ์และ Landmark จากแหล่งข้อมูลที่กำหนด
    :param source: "webcam" หรือ URL ของวิดีโอ YouTube
    :param save_video: True หากต้องการบันทึกวิดีโอ
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if source == "webcam":
        input_source = 0
        output_path = os.path.join(output_webcam_dir, f"EmotionandLandmarkWebcam_{timestamp}.mp4")
    elif source.startswith("https://www.youtube.com/") or source.startswith("https://youtu.be/"):
        input_source = source  # YouTube URL
        output_path = os.path.join(output_ytvideo_dir, f"YouTubeEmotion_{timestamp}.mp4")
    else:
        print("\n❌ ERROR: Invalid input source!")
        return

    print("\n✅ Debug: Initializing Camera...")
    cap = cv2.VideoCapture(input_source)

    # ✅ ตรวจสอบว่าเปิดกล้องได้หรือไม่ (Timeout 5 วินาที)
    timeout = 5
    start_time = datetime.datetime.now()

    while not cap.isOpened():
        if (datetime.datetime.now() - start_time).seconds > timeout:
            print("\n❌ ERROR: Camera not responding! Check if it's being used by another app.")
            return
        print("⏳ Waiting for camera to be available...")
        cv2.waitKey(1000)

    # ✅ ตรวจสอบขนาดวิดีโอและตั้งค่าบันทึก
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height)) if save_video else None

    print("\n✅ Debug: Camera ready. Starting Emotion Recognition...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("\n❌ ERROR: Cannot read frame from camera!")
            break

        frame = detect_emotion(frame)
        frame = detect_landmarks(frame)
        
        if save_video and out is not None:
            out.write(frame)

        cv2.imshow("Emotion Recognition & Landmark Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if save_video and out is not None:
        out.release()
        print(f"\n✅ Video saved at: {output_path}")

    cv2.destroyAllWindows()
