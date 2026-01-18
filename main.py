import streamlit as st
import yt_dlp
import os
import shutil

# --- 1. ページ基本設定とデザイン ---
st.set_page_config(page_title="SC Downloader", page_icon="🎵", layout="centered")

# 背景画像とカスタムCSSの設定
def apply_custom_design():
    # 好きな背景画像のURL（Unsplashの音楽イメージをデフォルトにしています）
    bg_image_url = "https://pbs.twimg.com/media/G-7FrWKXMAAXkc2?format=jpg&name=large"
    
    st.markdown(f"""
        <style>
        /* 背景画像の設定 */
        .stApp {{
            background-image: url("{bg_image_url}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}

        /* 全体にかけるオーバーレイ（文字を見やすくするため） */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.6); /* 黒い半透明の膜 */
            z-index: -1;
        }}

        /* 入力欄やテキストの色を白に固定 */
        h1, p, label {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}

        /* ボタンのデザイン（SoundCloudオレンジ） */
        div.stButton > button:first-child {{
            background-color: #ff5500;
            color: white;
            border-radius: 30px;
            border: none;
            font-weight: bold;
            padding: 0.5rem 2rem;
            transition: 0.3s;
        }}
        div.stButton > button:first-child:hover {{
            background-color: #ff8800;
            transform: scale(1.05);
        }}
        </style>
    """, unsafe_allow_html=True)

apply_custom_design()

# --- 2. メインコンテンツ ---
st.title("🎵 SC Downloader Pro")
st.write("SoundCloudのURLを入力して、最高音質のMP3を取得します。")

# サイドバーに使いかたを表示
with st.sidebar:
    st.header("Help & Info")
    st.info("1. SoundCloudで曲のURLをコピー\\n2. 下の欄に貼り付け\\n3. 準備ができたら保存ボタンをクリック")
    st.warning("⚠️ 私的利用の範囲内で使用してください。")

# 保存用ディレクトリ
temp_dir = "downloads"

# 入力欄
url = st.text_input("URLをペーストしてください", placeholder="https://soundcloud.com/...")

if st.button("Download Start"):
    if not url:
        st.error("URLを入力してください。")
    else:
        # 古いファイルを削除
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        with st.spinner("サーバーで処理中..."):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'writethumbnail': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {'key': 'FFmpegMetadata'},
                    {'key': 'EmbedThumbnail'},
                ],
                'quiet': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # ファイル名の取得（変換後を考慮）
                    files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
                    
                    if files:
                        target_file = os.path.join(temp_dir, files[0])
                        
                        # プレビュー再生
                        with open(target_file, "rb") as f:
                            st.audio(f.read(), format="audio/mp3")
                        
                        # ダウンロードボタン
                        with open(target_file, "rb") as f:
                            st.download_button(
                                label="Download MP3",
                                data=f,
                                file_name=os.path.basename(target_file),
                                mime="audio/mpeg"
                            )
                        st.balloons() # 成功のお祝い
                        st.success("ダウンロードの準備ができました！")
                    else:
                        st.error("変換に失敗しました。URLを確認してください。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

st.markdown("---")
st.caption("Powered by yt-dlp & Streamlit")
