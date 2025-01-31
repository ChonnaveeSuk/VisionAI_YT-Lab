import cv2
from ultralytics import YOLO

# โหลด YOLOv8 model
model = YOLO('yolov8n.pt')

# เปิด Webcam
cap = cv2.VideoCapture(0)

# ตั้งค่าการบันทึกวิดีโอ
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_webcam_detected.mp4', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ Debug: ไม่สามารถอ่านเฟรมได้")
        break

    # ใช้ YOLOv8 ตรวจจับวัตถุ
    results = model(frame)  # YOLOv8 prediction

    # ดึงผลลัพธ์จาก YOLOv8
    for result in results[0].boxes:
        x_min, y_min, x_max, y_max = result.xyxy[0].cpu().numpy()  # Bounding box
        label = result.cls[0].cpu().numpy()  # Class ID
        confidence = result.conf[0].cpu().numpy()  # Confidence

        # วาดกรอบและข้อความ
        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)  # วาดกรอบสีเขียว
        cv2.putText(frame, f"{label} {confidence:.2f}", (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # แสดงภาพ
    cv2.imshow("Object Detection", frame)

    # บันทึกวิดีโอ
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("✅ Debug: กด 'q' เพื่อออก")
        break

cap.release()
out.release()
cv2.destroyAllWindows()
