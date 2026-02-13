import streamlit as st
import datetime
import os
import json
import pandas as pd
import time

st.set_page_config(page_title="Study Coffee Pro+", page_icon="☕", layout="wide")

# =========================
# データ管理
# =========================

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
        "unlocked_sounds": ["デフォルトベル"],
        "current_sound": "デフォルトベル",
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

# =========================
# 画像設定
# =========================

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

# =========================
# サイドバー
# =========================

with st.sidebar:
    st.header("🌍 World Clock")

    now_utc = datetime.datetime.utcnow()
    jp = now_utc + datetime.timedelta(hours=9)
    ny = now_utc - datetime.timedelta(hours=5)

    st.write(f"🇯🇵 {jp.strftime('%H:%M')}  |  🇺🇸 {ny.strftime('%H:%M')}")
    st.divider()

    st.metric("My Beans", f"{st.session_state.user_data['total_beans']} 🫘")
    st.divider()

    st.subheader("🪄 模様替え")

    st.session_state.user_data["cafe_name"] = st.text_input(
        "カフェ名", st.session_state.user_data["cafe_name"]
    )

    for cat, mapping in [("壁紙", WALLPAPER_MAP), ("テーブル", TABLE_MAP)]:
        unlocked = st.session_state.user_data["unlocked_items"]
        options = [k for k in mapping if k in unlocked]
        current = st.session_state.user_data["current_items"].get(cat)
        idx = options.index(current) if current in options else 0

        st.session_state.user_data["current_items"][cat] = st.selectbox(
            f"{cat}選択", options, index=idx
        )

    if st.button("保存", use_container_width=True):
        save_data(st.session_state.user_data)
        st.rerun()

# =========================
# メインUI（コンテナ内だけ背景）
# =========================

current_bg = WALLPAPER_MAP[
    st.session_state.user_data["current_items"]["壁紙"]
]
current_tbl = TABLE_MAP[
    st.session_state.user_data["current_items"]["テーブル"]
]

st.markdown(f"""
<style>
.stApp {{
    background: #e8e8e8;
}}

.cafe-container {{
    background-image: url("{current_bg}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    padding: 50px;
    border-radius: 30px;
    margin: 30px auto;
    max-width: 1000px;
    backdrop-filter: blur(15px);
    box-shadow: 0 30px 70px rgba(0,0,0,0.4);
    color: white;
}}

.table-view {{
    background-image: url("{current_tbl}");
    background-size: cover;
    background-position: center;
    height: 300px;
    border-radius: 20px;
    margin: 30px 0;
    box-shadow: 0 15px 40px rgba(0,0,0,0.7);
}}

.glass {{
    background: rgba(0,0,0,0.5);
    padding: 20px;
    border-radius: 15px;
}}
</style>

<div class="cafe-container">
    <h1 style="font-size:3.5rem;margin:0;">
        {st.session_state.user_data["cafe_name"]}
    </h1>
    <div class="table-view"></div>
</div>
""", unsafe_allow_html=True)

# =========================
# タブ機能
# =========================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["⏲️ Timer", "⏱️ Watch", "💤 Sleep", "🛒 Shop", "📊 Log"]
)

# -------------------------
# タイマー（軽量リアル方式）
# -------------------------

with tab1:
    st.subheader("25分ポモドーロ")

    duration = 25 * 60

    if "end_time" not in st.session_state:
        st.session_state.end_time = None

    if st.button("スタート"):
        st.session_state.end_time = time.time() + duration

    if st.session_state.end_time:
        remaining = int(st.session_state.end_time - time.time())

        if remaining > 0:
            mm, ss = divmod(remaining, 60)
            st.metric("残り時間", f"{mm:02d}:{ss:02d}")
            st.experimental_rerun()
        else:
            st.success("☕ 勉強完了！ +5 Beans")
            st.session_state.user_data["total_beans"] += 5
            save_data(st.session_state.user_data)
            st.session_state.end_time = None
            st.balloons()

# -------------------------
# ストップウォッチ
# -------------------------

with tab2:
    st.subheader("自由計測")

    if "sw_start" not in st.session_state:
        st.session_state.sw_start = None

    col1, col2 = st.columns(2)

    if col1.button("開始"):
        st.session_state.sw_start = time.time()

    if col2.button("停止") and st.session_state.sw_start:
        elapsed = int((time.time() - st.session_state.sw_start) // 60)
        st.session_state.user_data["total_beans"] += elapsed // 5
        save_data(st.session_state.user_data)
        st.success(f"{elapsed}分記録！")
        st.session_state.sw_start = None

# -------------------------
# スリープ
# -------------------------

with tab3:
    minutes = st.number_input("スリープ（分）", 1, 120, 30)

    if st.button("開始"):
        st.info("タイマー起動中...")

# -------------------------
# ショップ
# -------------------------

with tab4:
    st.subheader("ショップ（簡易版）")
    st.write("今後拡張可能")

# -------------------------
# ログ
# -------------------------

with tab5:
    st.subheader("学習ログ")

    if st.session_state.user_data["logs"]:
        df = pd.DataFrame(st.session_state.user_data["logs"])
        st.dataframe(df)
    else:
        st.write("まだ記録がありません")
