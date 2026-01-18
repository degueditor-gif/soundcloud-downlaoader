import streamlit as st
import yt_dlp
import os
import shutil

# ページのタイトル設定
st.set_page_config(page_title="SC Downloader", page_icon="🎵")
st.title("🎵 SoundCloud Downloader")

# 保存用の一時ディレクトリ
temp_dir = "temp_downloads"

# URL入力欄
url = st.text_input("SoundCloudのURLを入力してください:", placeholder="https://soundcloud.com/...")

if st.button("ダウンロード開始"):
    if not url:
        st.warning("URLを入力してください。")
    else:
        # フォルダのクリーンアップ
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        with st.spinner("処理中...（曲の長さによっては時間がかかります）"):
            # yt-dlpのオプション
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {'key': 'FFmpegMetadata'},
                    {'key': 'EmbedThumbnail'},
                ],
                'writethumbnail': True,
                'quiet': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 情報の取得とダウンロード
                    info = ydl.extract_info(url, download=True)
                    # 実際に作成されたファイル名を特定
                    filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                    
                    # フォルダ内のmp3ファイルを探す（確実な方法）
                    files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
                    if files:
                        target_file = os.path.join(temp_dir, files[0])
                        
                        with open(target_file, "rb") as f:
                            st.audio(f.read(), format="audio/mp3") # ブラウザで試聴可能にする
                            
                        with open(target_file, "rb") as f:
                            st.download_button(
                                label="MP3をパソコンに保存",
                                data=f,
                                file_name=os.path.basename(target_file),
                                mime="audio/mpeg"
                            )
                        st.success("準備が完了しました！上のボタンから保存してください。")
                    else:
                        st.error("ファイルの変換に失敗しました。")

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

st.markdown("---")
st.caption("※私的利用の範囲内でご利用ください。")