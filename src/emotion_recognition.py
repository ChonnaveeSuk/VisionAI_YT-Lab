import cv2
import mediapipe as mp
import os
import datetime
from telebot import TeleBot
from dotenv import load_dotenv
from deepface import DeepFace
from youtube_downloader import download_youtube_video  # ✅ ใช้สำหรับดาวน์โหลดวิดีโอ YouTube

# ✅ โหลด Token ของ Telegram Bot
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ ตรวจสอบโฟลเดอร์สำหรับบันทึกวิดีโอ
output_dir = "C:/Vision_AI_YT/Output_Processed"
os.makedirs(output_dir, exist_ok=True)

# ✅ กำหนด Mediapipe FaceMesh และ Holistic (ตรวจจับร่างกายเต็มตัว)
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)
holistic = mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# ✅ กำหนดสีของ Landmark แต่ละส่วนให้แตกต่างกัน
LANDMARK_COLORS = {
    "face": (0, 255, 0),        # สีเขียว
    "left_hand": (255, 0, 255), # สีม่วง
    "right_hand": (255, 140, 0), # สีส้ม
    "pose": (0, 165, 255),       # สีส้มเข้ม
    "legs": (0, 255, 255)        # สีเหลือง
}

# ✅ กำหนดสีของแต่ละอารมณ์
EMOTION_COLORS = {
    "happy": (0, 255, 0),       # สีเขียว
    "angry": (0, 0, 255),       # สีแดง
    "surprise": (255, 255, 0),  # สีฟ้า
    "sad": (255, 0, 0),         # สีฟ้าเข้ม
    "neutral": (200, 200, 200)  # สีเทา
}

# ✅ ฟังก์ชันตรวจจับอารมณ์ด้วย DeepFace
def detect_emotion(face_crop):
    try:
        result = DeepFace.analyze(face_crop, actions=['emotion'], enforce_detection=False)
        if not result or not isinstance(result, list) or len(result) == 0:
            raise ValueError("No face detected")

        result = result[0]  
        emotion = result['dominant_emotion']
        confidence = result['emotion'][emotion]
        return emotion, confidence
    except Exception as e:
        print(f"❌ ERROR: DeepFace failed - {e}")
        return "neutral", 50.0  

# ✅ ฟังก์ชันวาด Bounding Box รอบใบหน้า
def draw_face_bounding_box(frame, face_detections):
    if face_detections:
        for detection in face_detections:
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

            face_crop = frame[y:y + h_box, x:x + w_box]
            emotion, confidence = detect_emotion(face_crop)

            color = EMOTION_COLORS.get(emotion, (255, 255, 255))
            label = f"{emotion.capitalize()} {confidence:.2f}%"
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

# ✅ ฟังก์ชันวาด Landmark ของใบหน้าแบบละเอียด
def draw_face_landmarks(frame, face_mesh_results):
    if face_mesh_results.multi_face_landmarks:
        for face_landmarks in face_mesh_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                face_landmarks, 
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=LANDMARK_COLORS["face"], thickness=1, circle_radius=1)
            )

# ✅ ฟังก์ชันวาด Landmark ของร่างกาย
def draw_body_landmarks(frame, results):
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=LANDMARK_COLORS["pose"], thickness=2, circle_radius=2)
        )

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=LANDMARK_COLORS["left_hand"], thickness=2, circle_radius=2)
        )
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=LANDMARK_COLORS["right_hand"], thickness=2, circle_radius=2)
        )

# ✅ ฟังก์ชันหลักสำหรับ Emotion Recognition (เพิ่มการรองรับ YouTube)
def recognize_emotions(source="webcam", save_video=False, youtube_url=None, chat_id=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(output_dir, f"Emotion_Detection_{timestamp}.mp4")

    if source == "youtube":
        video_path = download_youtube_video(youtube_url)  # ✅ ดาวน์โหลดวิดีโอ YouTube
        cap = cv2.VideoCapture(video_path)
    else:
        cap = cv2.VideoCapture(0)  # ✅ ไม่เปลี่ยนแปลง `/webcam`

    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height)) if save_video else None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_detection.process(rgb_frame)
        draw_face_bounding_box(frame, face_results.detections)

        face_mesh_results = face_mesh.process(rgb_frame)
        draw_face_landmarks(frame, face_mesh_results)

        results = holistic.process(rgb_frame)
        draw_body_landmarks(frame, results)

        if save_video:
            out.write(frame)

        cv2.imshow("Emotion Recognition & Landmark Detection", frame)

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
