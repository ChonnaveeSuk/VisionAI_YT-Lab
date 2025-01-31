import yt_dlp
import os
import json
import pandas as pd

# ✅ กำหนดโฟลเดอร์สำหรับบันทึกข้อมูล YouTube
yt_info_dir = "C:/Vision_AI_YT/Youtube_Video_Info"
yt_video_dir = "C:/Vision_AI_YT/Output_YTvideo"
os.makedirs(yt_info_dir, exist_ok=True)
os.makedirs(yt_video_dir, exist_ok=True)

# ✅ ฟังก์ชันดึงข้อมูลวิดีโอ YouTube
def get_video_info(youtube_url):
    """
    ดึงข้อมูลวิดีโอจาก YouTube โดยไม่ต้องดาวน์โหลด
    :param youtube_url: ลิงก์ YouTube
    :return: ดิกชันนารีข้อมูลวิดีโอ หรือ None หากเกิดข้อผิดพลาด
    """
    if not youtube_url.startswith("https://www.youtube.com/") and not youtube_url.startswith("https://youtu.be/"):
        print("❌ ERROR: Invalid YouTube URL!")
        return None

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,  # ไม่ต้องดาวน์โหลดวิดีโอ
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

        video_info = {
            "Title": info.get("title", "Unknown Title"),
            "Channel": info.get("uploader", "Unknown Channel"),
            "Views": info.get("view_count", 0),
            "Likes": info.get("like_count", "N/A"),
            "Comments": info.get("comment_count", "N/A"),
            "Duration": info.get("duration", 0),
            "URL": youtube_url
        }

        # ✅ บันทึกข้อมูลลงไฟล์ JSON และ CSV
        video_title_safe = video_info["Title"].replace(" ", "_")
        json_path = os.path.join(yt_info_dir, f"{video_title_safe}_info.json")
        csv_path = os.path.join(yt_info_dir, f"{video_title_safe}_info.csv")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(video_info, f, indent=4)

        df = pd.DataFrame([video_info])
        df.to_csv(csv_path, index=False)

        print(f"✅ INFO: YouTube data saved at {json_path}")
        return video_info

    except Exception as e:
        print(f"❌ ERROR: Failed to fetch video info! {e}")
        return None

# ✅ ฟังก์ชันดาวน์โหลดวิดีโอ YouTube
def download_youtube_video(youtube_url):
    """
    ดาวน์โหลดวิดีโอจาก YouTube
    :param youtube_url: ลิงก์ YouTube
    :return: เส้นทางไฟล์วิดีโอ หรือ None หากเกิดข้อผิดพลาด
    """
    if not youtube_url.startswith("https://www.youtube.com/") and not youtube_url.startswith("https://youtu.be/"):
        print("❌ ERROR: Invalid YouTube URL!")
        return None

    output_path = os.path.join(yt_video_dir, "youtube_video.mp4")

    # ✅ ลบไฟล์เก่าหากมีอยู่ เพื่อป้องกันคลิปซ้ำ
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
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        print(f"✅ DOWNLOAD: YouTube video saved at {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ ERROR: Failed to download video! {e}")
        return None

# ✅ ฟังก์ชันทดสอบการทำงาน
if __name__ == "__main__":
    print("✅ Debug: youtube_downloader.py ทำงานแล้ว")

    test_url = input("🎥 กรุณาป้อนลิงก์ YouTube: ").strip()
    info = get_video_info(test_url)
    
    if info:
        download = input("📥 ต้องการดาวน์โหลดวิดีโอหรือไม่? (y/n): ").strip().lower()
        if download == "y":
            download_youtube_video(test_url)
