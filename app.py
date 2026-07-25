import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="TikTok Song Finder", page_icon="🎵", layout="centered"
)

st.title("🎵 TikTok Song Finder")
st.write("วางลิงก์คลิป TikTok ด้านล่างเพื่อค้นหาชื่อเพลงในคลิป")

tiktok_url = st.text_input(
    "วางลิงก์ TikTok ที่นี่:", placeholder="https://www.tiktok.com/..."
)

if st.button("🔍 ค้นหาชื่อเพลง"):
    if tiktok_url:
        try:
            ydl_opts = {
                "quiet": True,
                "skip_download": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(tiktok_url, download=False)
                track = info.get("track")
                artist = info.get("artist")
                title = info.get("title")

                st.success("ค้นหาสำเร็จ!")
                if track or artist:
                    st.subheader(f"🎶 เพลง: {track or 'ไม่ทราบชื่อเพลง'}")
                    st.write(f"🎤 ศิลปิน: {artist or 'ไม่ทราบศิลปิน'}")
                else:
                    st.write(f"📌 ชื่อคลิป/เสียงประกอบ: {title}")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกลิงก์ก่อนครับ")
