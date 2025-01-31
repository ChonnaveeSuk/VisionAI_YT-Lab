import yt_dlp

def get_video_info():
    """
    ให้ผู้ใช้ป้อนลิงก์ YouTube แล้วดึงข้อมูลวิดีโอ
    """
    url = input("🎥 กรุณาป้อนลิงก์ YouTube: ").strip()

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,  # ไม่ต้องดาวน์โหลดวิดีโอ
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        print("\n🎥 ข้อมูลวิดีโอจาก YouTube:")
        print(f"🔹 ชื่อวิดีโอ: {info['title']}")
        print(f"🔹 ชื่อช่อง: {info['uploader']}")
        print(f"🔹 ยอดวิว: {info['view_count']}")
        print(f"🔹 ยอดไลก์: {info.get('like_count', 'N/A')}")
        print(f"🔹 จำนวนคอมเมนต์: {info.get('comment_count', 'N/A')}")
        print(f"🔹 ความยาววิดีโอ: {info['duration']} วินาที")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

# ทดสอบการทำงาน
if __name__ == "__main__":
    print("✅ Debug: youtube_downloader.py ทำงานแล้ว")
    get_video_info()
