import urllib.parse
import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="TikTok Song Finder", page_icon="🎵", layout="centered"
)

st.title("🎵 TikTok Song Finder")
st.write("วางลิงก์คลิป TikTok เพื่อดึงชื่อเพลงไปฟังต่อบน Spotify")

tiktok_url = st.text_input(
    "วางลิงก์ TikTok ที่นี่:", placeholder="https://www.tiktok.com/..."
)

if st.button("🔍 ค้นหาชื่อเพลง"):
    if tiktok_url:
        with st.spinner("กำลังดึงข้อมูลเพลง..."):
            try:
                ydl_opts = {
                    "quiet": True,
                    "skip_download": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(tiktok_url, download=False)

                    # ดึงชื่อเพลง ศิลปิน หรือชื่อคลิป
                    track = info.get("track")
                    artist = info.get("artist")
                    title = info.get("title", "")

                    # จัดการชื่อเพลงให้อ่านง่ายที่สุด
                    if track and artist:
                        song_name = f"{track} - {artist}"
                    elif track:
                        song_name = track
                    else:
                        song_name = title

                    st.success("ดึงข้อมูลสำเร็จ!")

                    # แสดงชื่อเพลงให้คัดลอกง่ายๆ
                    st.subheader("📌 ชื่อเพลง / คีย์เวิร์ดสำหรับค้นหา:")
                    st.code(song_name, language="text")

                    # สร้างลิงก์ตรงสำหรับเปิดค้นหาใน Spotify
                    encoded_query = urllib.parse.quote(song_name)
                    spotify_url = f"https://open.spotify.com/search/{encoded_query}"

                    st.markdown("---")
                    st.link_button(
                        "🟢 คลิกเพื่อไปค้นหาบน Spotify ทันที",
                        spotify_url,
                        use_container_width=True,
                    )

            except Exception as e:
                st.error(
                    "เกิดข้อผิดพลาดในการดึงข้อมูล กรุณาตรวจสอบว่าเป็นลิงก์คลิปวิดีโอ TikTok ปกติครับ"
                )
    else:
        st.warning("กรุณากรอกลิงก์ TikTok ก่อนครับ")
