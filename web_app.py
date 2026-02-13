import streamlit as st
import time
import datetime
import os
import json
import random

# --- 1. ページ設定 ---
st.set_page_config(page_title="Study Coffee Pro+", page_icon="☕", layout="wide")

# --- 2. データ保存・読み込み (JSON) ---
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 初期データの補完
            defaults = {
                "total_beans": 0, "logs": [], "cafe_name": "My Coffee",
                "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル",
                "unlocked_items": ["白壁", "丸太のテーブル", "なし"], 
                "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁", "看板": "なし"}
            }
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
    return {"total_beans": 0, "logs": [], "cafe_name": "My Coffee", "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル", "unlocked_items": ["白壁", "丸太のテーブル", "なし"], "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁", "看板": "なし"}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

# --- 3. 高品質ビジュアル & ショップ定義 ---
WALLPAPER_MAP = {
    "白壁": "https://images.unsplash.com",
    "レンガのカフェ": "https://images.unsplash.com",
    "森のテラス": "https://images.unsplash.com",
    "深夜の読書室": "https://images.unsplash.com"
}

TABLE_MAP = {
    "丸太のテーブル": "https://images.unsplash.com",
    "大理石の机": "https://images.unsplash.com",
    "アンティーク机": "https://images.unsplash.com"
}

SIGN_MAP = {
    "なし": "",
    "ネオンサイン": "https://images.unsplash.com",
    "黒板メニュー": "https://images.unsplash.com"
}

INTERIOR_SHOP = {
    "壁紙": {"レンガのカフェ": 15, "森のテラス": 25, "深夜の読書室": 40},
    "テーブル": {"大理石の机": 20, "アンティーク机": 40},
    "看板": {"ネオンサイン": 30, "黒板メニュー": 15}
}

SOUND_LIBRARY = {
    "デフォルトベル": "https://www.soundjay.com",
    "カフェの喧騒": "https://www.soundjay.com",
    "森の鳥": "https://www.soundjay.com"
}

STUDY_TRIVIA = ["青いペンは記憶力を高める", "15分単位の集中が効率的", "試験前の昼寝は有効"]
COFFEE_TRIVIA = ["コーヒーは元々薬だった", "香りはリラックス効果がある", "豆は実は種子"]
PRAISE_MSGS = ["天才すぎ！", "最高！", "神集中！"]

# --- 4. 共通ロジック ---
def play_alarm():
    url = SOUND_LIBRARY.get(st.session_state.user_data.get("current_sound", "デフォルトベル"))
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

def complete_session(mode, minutes, is_study=True):
    beans = minutes // 10 if is_study else 0
    st.session_state.user_data["total_beans"] += beans
    st.session_state.user_data["logs"].append({"date": datetime.datetime.now().strftime('%m/%d %H:%M'), "mode": mode, "min": minutes})
    save_data(st.session_state.user_data)
    play_alarm()
    if is_study: st.balloons()

# --- 5. メインUI ---
# サイドバー
with st.sidebar:
    st.header("🌍 World Clock")
    now = datetime.datetime.now()
    st.write(f"🇯🇵 {now.strftime('%H:%M')} | 🇺🇸 {(now - datetime.timedelta(hours=14)).strftime('%H:%M')}")
    st.divider()
    st.metric("My Beans", f"{st.session_state.user_data['total_beans']} 🫘")
    
    st.subheader("🛠️ 模様替え")
    st.session_state.user_data["cafe_name"] = st.text_input("カフェの名前", st.session_state.user_data["cafe_name"])
    for cat in ["壁紙", "テーブル", "看板"]:
        opts = [i for i in st.session_state.user_data["unlocked_items"] if i in INTERIOR_SHOP.get(cat, {}) or i in ["白壁", "丸太のテーブル", "なし"]]
        st.session_state.user_data["current_items"][cat] = st.selectbox(f"{cat}", opts)
    
    st.subheader("🎵 音設定")
    st.session_state.user_data["current_sound"] = st.selectbox("Alarm Sound", st.session_state.user_data["unlocked_sounds"])
    
    if st.button("設定を保存"):
        save_data(st.session_state.user_data)
        st.rerun()

# カフェビジュアル描画
items = st.session_state.user_data["current_items"]
bg = WALLPAPER_MAP.get(items["壁紙"], WALLPAPER_MAP["白壁"])
tbl = TABLE_MAP.get(items["テーブル"], TABLE_MAP["丸太のテーブル"])
sgn = SIGN_MAP.get(items["看板"], "")

st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg}"); background-size: cover; background-position: center; }}
    .cafe-card {{
        background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(8px);
        padding: 30px; border-radius: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.2);
    }}
    .sign-img {{ width: 120px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 0 15px white; }}
    .table-img {{ width: 250px; border-radius: 15px; margin-top: 15px; border-bottom: 8px solid #222; }}
    </style>
    <div class="cafe-card">
        {f'<img src="{sgn}" class="sign-img">' if sgn else ''}
        <h1 style="color: white; text-shadow: 2px 2px 8px black; margin:0;">{st.session_state.user_data["cafe_name"]}</h1>
        <img src="{tbl}" class="table-img">
        <p style="color: white; font-size: 20px; margin-top:10px;">☕ 📖 Studying... <span style="animation: blink 1s infinite;">_</span></p>
    </div>
    <style> @keyframes blink {{ 0%{{opacity:0;}} 50%{{opacity:1;}} 100%{{opacity:0;}} }} </style>
    """, unsafe_allow_html=True)

# タブ機能
t1, t2, t3, t4, t5 = st.tabs(["⏲️ Timer", "⏱️ Watch", "💤 Sleep", "🛒 Shop", "📊 Log"])

with t1: # Timer
    m_choice = st.radio("Mode", ["勉強 (25分)", "休憩 (5分)"], horizontal=True)
    memo = st.text_input("Alarm Memo")
    if st.button("Start Timer"):
        t_m = 25 if "勉強" in m_choice else 5
        ph = st.empty()
        st.info(f"💡 {random.choice(STUDY_TRIVIA if '勉強' in m_choice else COFFEE_TRIVIA)}")
        for t in range(t_m * 60, -1, -1):
            mm, ss = divmod(t, 60)
            ph.metric("Remaining", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        complete_session(m_choice, t_m, "勉強" in m_choice)
        if memo: st.warning(f"📝 {memo}")

with t2: # Watch
    sw_ph = st.empty()
    c1, c2 = st.columns(2)
    if c1.button("Start"):
        st.session_state.sw_start = time.time()
        st.session_state.sw_run = True
    if c2.button("Stop & Save"):
        if "sw_start" in st.session_state:
            el = int((time.time() - st.session_state.sw_start) // 60)
            complete_session("自由計測", el, True)
            st.session_state.sw_run = False
            st.rerun()
    if st.session_state.get("sw_run", False):
        while st.session_state.sw_run:
            df = int(time.time() - st.session_state.sw_start); mm, ss = divmod(df, 60)
            sw_ph.metric("Elapsed", f"{mm:02d}:{ss:02d}"); time.sleep(1)

with t3: # Sleep
    sl_m = st.number_input("アラーム設定（分）", 1, 120, 60)
    if st.button("Sleep Start"):
        ph = st.empty()
        for t in range(sl_m * 60, -1, -1):
            mm, ss = divmod(t, 60); ph.metric("あと", f"{mm:02d}:{ss:02d}"); time.sleep(1)
        play_alarm(); st.error("⏰ Wake Up!")

with t4: # Shop
    for cat, items in INTERIOR_SHOP.items():
        st.subheader(f"🛒 {cat}")
        cols = st.columns(3)
        for i, (name, price) in enumerate(items.items()):
            with cols[i % 3]:
                owned = name in st.session_state.user_data["unlocked_items"]
                if st.button(f"{name}\n({price}🫘)", key=f"s_{name}", disabled=owned):
                    if st.session_state.user_data["total_beans"] >= price:
                        st.session_state.user_data["total_beans"] -= price
                        st.session_state.user_data["unlocked_items"].append(name)
                        save_data(st.session_state.user_data); st.rerun()
                    else: st.error("豆不足！")

with t5: # Log
    st.subheader("📚 Log")
    for log in reversed(st.session_state.user_data["logs"]):
        st.text(f"📅 {log['date']} | {log['mode']} | {log['min']}min")
