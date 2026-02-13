import streamlit as st
import time
import datetime
import os
import json
import random

# --- 1. ページ設定 ---
st.set_page_config(page_title="Study Coffee Pro+", page_icon="☕", layout="wide")

# --- 2. データの保存と読み込み ---
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 項目が足りない場合の初期設定
            defaults = {
                "total_beans": 0, "logs": [], "cafe_name": "My Coffee",
                "unlocked_items": ["白壁", "丸太のテーブル", "なし"], 
                "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁", "看板": "なし"},
                "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル"
            }
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
    return {
        "total_beans": 0, "logs": [], "cafe_name": "My Coffee",
        "unlocked_items": ["白壁", "丸太のテーブル", "なし"], 
        "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁", "看板": "なし"},
        "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル"
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

# --- 3. ショップ・ビジュアル素材 ---
WALLPAPER_MAP = {
    "白壁": "https://images.unsplash.com",
    "レンガのカフェ": "https://images.unsplash.com",
    "森のテラス": "https://images.unsplash.com",
    "深夜の読書室": "https://images.unsplash.com",
    "近未来ラボ": "https://images.unsplash.com"
}

TABLE_MAP = {
    "丸太のテーブル": "https://images.unsplash.com",
    "大理石の机": "https://images.unsplash.com",
    "アンティーク机": "https://images.unsplash.com",
    "ゲーミングデスク": "https://images.unsplash.com"
}

SOUND_LIBRARY = {
    "デフォルトベル": "https://www.soundjay.com",
    "カフェの喧騒": "https://www.soundjay.com",
    "森の鳥": "https://www.soundjay.com"
}

INTERIOR_SHOP = {
    "壁紙": {"レンガのカフェ": 15, "森のテラス": 25, "深夜の読書室": 40, "近未来ラボ": 50},
    "テーブル": {"大理石の机": 20, "アンティーク机": 40, "ゲーミングデスク": 60},
    "音": {"カフェの喧騒": 10, "森の鳥": 20}
}

# --- 4. 時間連動（夜になると暗くなる） ---
def get_time_style():
    hour = datetime.datetime.now().hour
    if 18 <= hour or hour < 6:
        return "rgba(0, 0, 50, 0.4)" # 夜：青暗い
    elif 16 <= hour < 18:
        return "rgba(255, 100, 0, 0.2)" # 夕方：オレンジ
    else:
        return "rgba(0, 0, 0, 0)" # 昼：透明

# --- 5. サイドバー (世界時計・模様替え) ---
with st.sidebar:
    st.header("🌍 World Clock")
    now = datetime.datetime.now()
    st.write(f"🇯🇵 JP: {now.strftime('%H:%M')} | 🇺🇸 NY: {(now - datetime.timedelta(hours=14)).strftime('%H:%M')}")
    st.divider()
    
    st.metric("My Beans", f"{st.session_state.user_data['total_beans']} 🫘")
    
    st.divider()
    st.subheader("🪄 模様替え")
    st.session_state.user_data["cafe_name"] = st.text_input("カフェの名前", st.session_state.user_data["cafe_name"])
    
    for cat in ["壁紙", "テーブル"]:
        options = [i for i in st.session_state.user_data["unlocked_items"] if i in INTERIOR_SHOP.get(cat, {}) or i in ["白壁", "丸太のテーブル"]]
        st.session_state.user_data["current_items"][cat] = st.selectbox(f"{cat}を選択", options, key=f"select_{cat}")
    
    st.session_state.user_data["current_sound"] = st.selectbox("アラーム音", st.session_state.user_data["unlocked_sounds"])

    if st.button("設定を保存して更新"):
        save_data(st.session_state.user_data)
        st.rerun()

# --- 6. カフェ画面の描画 ---
items = st.session_state.user_data["current_items"]
bg_img = WALLPAPER_MAP.get(items["壁紙"], WALLPAPER_MAP["白壁"])
tbl_img = TABLE_MAP.get(items["テーブル"], TABLE_MAP["丸太のテーブル"])
overlay_color = get_time_style()

# unsafe_allow_html=True を使い、画像のようなバグを修正
st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_img}"); background-size: cover; background-position: center; }}
    .night-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: {overlay_color}; pointer-events: none; z-index: 1; }}
    .cafe-container {{
        background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px);
        padding: 40px; border-radius: 20px; text-align: center; color: white;
        border: 1px solid rgba(255,255,255,0.2); position: relative; z-index: 2;
    }}
    .table-img {{ width: 250px; border-radius: 15px; margin: 20px 0; border-bottom: 8px solid #222; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}
    @keyframes blink {{ 0%{{opacity:0;}} 50%{{opacity:1;}} 100%{{opacity:0;}} }}
    .blink {{ animation: blink 1.5s infinite; }}
    </style>
    <div class="night-overlay"></div>
    <div class="cafe-container">
        <h1 style="text-shadow: 2px 2px 8px black; margin:0;">{st.session_state.user_data["cafe_name"]}</h1>
        <img src="{tbl_img}" class="table-img">
        <p style="font-size: 20px;">☕ Studying... <span class="blink">_</span></p>
    </div>
    """, unsafe_allow_html=True)

# --- 7. 各機能タブ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⏲️ Timer", "⏱️ Watch", "💤 Sleep", "🛒 Shop", "📊 Log"])

def play_alarm():
    sound_url = SOUND_LIBRARY.get(st.session_state.user_data.get("current_sound", "デフォルトベル"))
    st.components.v1.html(f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>', height=0)

with tab1: # ポモドーロタイマー
    col1, col2 = st.columns(2)
    with col1:
        mode = st.radio("モード", ["勉強 (25分)", "休憩 (5分)"], horizontal=True)
        memo = st.text_input("アラーム用メモ", placeholder="終わったらストレッチ！")
    
    if st.button("タイマー開始"):
        t_min = 25 if "勉強" in mode else 5
        ph = st.empty()
        for t in range(t_min * 60, -1, -1):
            mm, ss = divmod(t, 60)
            ph.metric("残り時間", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        # 完了処理
        st.session_state.user_data["total_beans"] += (t_min // 10 if "勉強" in mode else 0)
        st.session_state.user_data["logs"].append({"date": datetime.datetime.now().strftime('%m/%d %H:%M'), "mode": mode, "min": t_min})
        save_data(st.session_state.user_data)
        play_alarm()
        st.balloons() if "勉強" in mode else st.snow()
        if memo: st.warning(f"📝 メモ: {memo}")
        st.rerun()

with tab2: # ストップウォッチ
    st.subheader("⏱️ 自由計測")
    sw_ph = st.empty()
    c1, c2 = st.columns(2)
    if c1.button("計測開始", key="sw_start"):
        st.session_state.sw_start = time.time()
        st.session_state.sw_running = True
    if c2.button("ストップ & 保存", key="sw_stop"):
        if "sw_start" in st.session_state:
            elapsed = int((time.time() - st.session_state.sw_start) // 60)
            st.session_state.user_data["total_beans"] += (elapsed // 10)
            st.session_state.user_data["logs"].append({"date": datetime.datetime.now().strftime('%m/%d %H:%M'), "mode": "自由計測", "min": elapsed})
            save_data(st.session_state.user_data)
            st.session_state.sw_running = False
            st.success(f"{elapsed}分記録しました！")
            st.rerun()
    if st.session_state.get("sw_running", False):
        while st.session_state.sw_running:
            diff = int(time.time() - st.session_state.sw_start)
            mm, ss = divmod(diff, 60)
            sw_ph.metric("経過時間", f"{mm:02d}:{ss:02d}")
            time.sleep(1)

with tab3: # スリープタイマー
    s_min = st.number_input("アラーム設定（分）", 1, 120, 60)
    s_note = st.text_input("終了メッセージ", "起きて！")
    if st.button("スリープタイマー開始"):
        ph = st.empty()
        for t in range(s_min * 60, -1, -1):
            mm, ss = divmod(t, 60)
            ph.metric("あと", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        play_alarm()
        st.error(f"⏰ {s_note}")

with tab4: # ショップ
    st.subheader("🛒 インテリアショップ")
    st.write(f"現在の所持: {st.session_state.user_data['total_beans']} 🫘")
    for cat, items in INTERIOR_SHOP.items():
        st.write(f"#### {cat}")
        cols = st.columns(2)
        for i, (name, price) in enumerate(items.items()):
            with cols[i % 2]:
                is_owned = name in st.session_state.user_data["unlocked_items"] or name in st.session_state.user_data["unlocked_sounds"]
                if st.button(f"{name} ({price}🫘)", key=f"buy_{name}", disabled=is_owned):
                    if st.session_state.user_data["total_beans"] >= price:
                        st.session_state.user_data["total_beans"] -= price
                        if cat == "音": st.session_state.user_data["unlocked_sounds"].append(name)
                        else: st.session_state.user_data["unlocked_items"].append(name)
                        save_data(st.session_state.user_data)
                        st.success(f"{name} を購入しました！")
                        st.rerun()
                    else: st.error("豆が足りません！")

with tab5: # 履歴
    st.subheader("📊 学習記録")
    for log in reversed(st.session_state.user_data["logs"]):
        st.text(f"📅 {log['date']} | {log['mode']} | {log['min']}分")
