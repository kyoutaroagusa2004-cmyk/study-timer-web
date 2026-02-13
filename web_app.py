import streamlit as st
import time
import datetime
import os
import json

# --- 1. ページ設定 ---
st.set_page_config(page_title="Study Coffee Pro+", page_icon="☕", layout="wide")

# --- 2. データ保存 ---
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    defaults = {
        "total_beans": 0,
        "logs": [],
        "cafe_name": "My Coffee",
        "unlocked_items": ["白壁", "丸太のテーブル"],
        "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁"},
    }

    for k, v in defaults.items():
        if k not in data:
            data[k] = v

    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "user_data" not in st.session_state:
    st.session_state.user_data = load_data()

# --- 3. 画像URL（修正版） ---
WALLPAPER_MAP = {
    "白壁": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=1600&q=80",
    "レンガのカフェ": "https://images.unsplash.com/photo-1492724441997-5dc865305da7?auto=format&fit=crop&w=1600&q=80",
    "森のテラス": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1600&q=80",
    "深夜の読書室": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1600&q=80",
    "近未来ラボ": "https://images.unsplash.com/photo-1581091012184-7f7a3c8b9f8b?auto=format&fit=crop&w=1600&q=80",
}

TABLE_MAP = {
    "丸太のテーブル": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=1200&q=80",
    "大理石の机": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80",
    "アンティーク机": "https://images.unsplash.com/photo-1493666438817-866a91353ca9?auto=format&fit=crop&w=1200&q=80",
    "ゲーミングデスク": "https://images.unsplash.com/photo-1593642634367-d91a135587b5?auto=format&fit=crop&w=1200&q=80",
}

# --- 4. サイドバー ---
with st.sidebar:
    st.header("🌍 World Clock")

    now_utc = datetime.datetime.utcnow()
    jp_time = now_utc + datetime.timedelta(hours=9)
    ny_time = now_utc - datetime.timedelta(hours=5)

    st.write(f"🇯🇵 JP: {jp_time.strftime('%H:%M')} | 🇺🇸 NY: {ny_time.strftime('%H:%M')}")
    st.divider()

    st.metric("My Beans", f"{st.session_state.user_data['total_beans']} 🫘")
    st.divider()

    st.subheader("🪄 模様替え")

    st.session_state.user_data["cafe_name"] = st.text_input(
        "カフェの名前",
        st.session_state.user_data["cafe_name"]
    )

    for cat, mapping in [("壁紙", WALLPAPER_MAP), ("テーブル", TABLE_MAP)]:
        unlocked = st.session_state.user_data["unlocked_items"]
        options = [k for k in mapping.keys() if k in unlocked]
        current = st.session_state.user_data["current_items"].get(cat, options[0])
        idx = options.index(current) if current in options else 0

        st.session_state.user_data["current_items"][cat] = st.selectbox(
            f"{cat}を選択",
            options,
            index=idx
        )

    if st.button("設定を保存", use_container_width=True):
        save_data(st.session_state.user_data)
        st.rerun()

# --- 5. 背景CSS ---
current_bg = WALLPAPER_MAP[st.session_state.user_data["current_items"]["壁紙"]]
current_tbl = TABLE_MAP[st.session_state.user_data["current_items"]["テーブル"]]

st.markdown(f"""
<style>
.stApp {{
    background-image: url("{current_bg}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.cafe-container {{
    background: rgba(0,0,0,0.65);
    backdrop-filter: blur(15px);
    padding: 40px;
    border-radius: 30px;
    text-align: center;
    color: white;
    margin: 40px auto;
    max-width: 900px;
}}

.table-view {{
    background-image: url("{current_tbl}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 320px;
    border-radius: 20px;
    margin: 30px 0;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
}}

@keyframes blink {{
    0%{{opacity:0.3;}}
    50%{{opacity:1;}}
    100%{{opacity:0.3;}}
}}

.blink {{
    animation: blink 2s infinite;
    font-weight: bold;
    color: #f1c40f;
    font-size: 24px;
}}
</style>

<div class="cafe-container">
    <h1 style="font-size: 3.5rem; margin:0;">
        {st.session_state.user_data["cafe_name"]}
    </h1>
    <div class="table-view"></div>
    <div class="blink">☕ Studying...</div>
</div>
""", unsafe_allow_html=True)

# --- 6. タイマー ---
st.divider()
st.subheader("⏲️ 25分タイマー")

if st.button("スタート", use_container_width=True):
    placeholder = st.empty()
    for t in range(25*60, -1, -1):
        mm, ss = divmod(t, 60)
        placeholder.metric("残り時間", f"{mm:02d}:{ss:02d}")
        time.sleep(1)

    st.session_state.user_data["total_beans"] += 5
    st.session_state.user_data["logs"].append({
        "date": datetime.datetime.now().strftime('%m/%d %H:%M'),
        "min": 25
    })
    save_data(st.session_state.user_data)

    st.success("☕ 勉強完了！ +5 Beans")
    st.balloons()
    st.rerun()
