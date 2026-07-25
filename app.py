import asyncio
import os
from shazamio import Shazam
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


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "temp_audio",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "temp_audio.mp3"


async def find_song(audio_file):
    shazam = Shazam()
    return await shazam.recognize(audio_file)


if st.button("🔍 ค้นหาชื่อเพลง", type="primary"):
    if tiktok_url:
        with st.spinner("⏳ กำลังดึงเสียงจาก TikTok และค้นหาเพลง..."):
            try:
                audio_file = download_audio(tiktok_url)
                out = asyncio.run(find_song(audio_file))

                track = out.get("track")
                if track:
                    st.success("🎉 เจอเพลงแล้ว!")
                    st.header(f"🎵 {track.get('title')}")
                    st.subheader(f"👤 {track.get('subtitle')}")

                    images = track.get("images", {})
                    if images.get("coverart"):
                        st.image(images.get("coverart"), width=200)
                else:
                    st.warning("❌ ไม่พบข้อมูลเพลงในคลิปนี้")

                if os.path.exists(audio_file):
                    os.remove(audio_file)

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกลิงก์ TikTok ก่อนครับ")
