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
            defaults = {
                "total_beans": 0, "logs": [], 
                "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル",
                "unlocked_items": ["丸太のテーブル", "白壁"], 
                "current_items": {"テーブル": "丸太のテーブル", "壁": "白壁", "看板": "なし"}
            }
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
    return {
        "total_beans": 0, "logs": [], 
        "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル",
        "unlocked_items": ["丸太のテーブル", "白壁"], 
        "current_items": {"テーブル": "丸太のテーブル", "壁": "白壁", "看板": "なし"}
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

# --- 3. アラーム音 & インテリア定義 ---
SOUND_LIBRARY = {
    "デフォルトベル": "https://www.soundjay.com",
    "カフェの喧騒": "https://www.soundjay.com",
    "森の鳥": "https://www.soundjay.com",
    "デジタル時計": "https://www.soundjay.com"
}

INTERIOR_SHOP = {
    "音": {"カフェの喧騒": 10, "森の鳥": 20, "デジタル時計": 30},
    "壁": {"レンガの壁": 15, "木目調の壁": 25, "星空の壁": 50},
    "テーブル": {"大理石の机": 20, "アンティーク机": 40, "ゲーミングデスク": 60},
    "看板": {"ネオンサイン": 30, "黒板メニュー": 10}
}

STYLE_MAP = {
    "壁": {"白壁": "#f9f9f9", "レンガの壁": "#b22222", "木目調の壁": "#deb887", "星空の壁": "#000033"},
    "テーブル": {"丸太のテーブル": "🟫", "大理石の机": "⬜", "アンティーク机": "🪵", "ゲーミングデスク": "⬛"}
}

def play_alarm():
    sound_url = SOUND_LIBRARY.get(st.session_state.user_data.get("current_sound", "デフォルトベル"))
    st.components.v1.html(f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>', height=0)

# --- 4. 雑学 & 褒め言葉 ---
STUDY_TRIVIA = ["青いペンで書くと記憶力が上がる説がある", "試験直前の昼寝は記憶の整理に有効", "独り言学習は効率UP"]
COFFEE_TRIVIA = ["コーヒーは元々『薬』だった", "香りはリラックス効果抜群", "世界で2番目に多く飲まれる飲み物"]
PRAISE_MSGS = ["天才すぎる！", "その調子！", "努力の天才！", "集中力、神レベル！"]

# --- 5. 共通処理 ---
def complete_session(mode_name, minutes, is_study=True):
    beans = minutes // 10 if is_study else 0
    st.session_state.user_data["total_beans"] += beans
    st.session_state.user_data["logs"].append({"date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), "mode": mode_name, "min": minutes})
    save_data(st.session_state.user_data)
    play_alarm()
    if is_study:
        st.balloons()
        st.success(f"🎉 {random.choice(PRAISE_MSGS)} {beans}粒獲得！")

# --- 6. メインUI ---
# サイドバー
with st.sidebar:
    st.header("🌍 世界時計")
    now = datetime.datetime.now()
    st.write(f"🇯🇵 日本: {now.strftime('%H:%M')}")
    st.write(f"🇺🇸 NY: {(now - datetime.timedelta(hours=14)).strftime('%H:%M')}")
    st.divider()
    st.metric("現在の所持数", f"{st.session_state.user_data['total_beans']} 🫘 豆")
    st.subheader("🎵 音設定")
    st.session_state.user_data["current_sound"] = st.selectbox("使用する音", st.session_state.user_data["unlocked_sounds"])
    st.subheader("🛠️ 模様替え")
    for cat in ["壁", "テーブル", "看板"]:
        options = [i for i in st.session_state.user_data["unlocked_items"] if i in INTERIOR_SHOP.get(cat, {}) or i in ["白壁", "丸太のテーブル", "なし"]]
        st.session_state.user_data["current_items"][cat] = st.selectbox(f"{cat}", options, key=f"side_{cat}")

# タブ構成
tab0, tab1, tab2, tab3, tab4 = st.tabs(["🏠 マイカフェ", "⏲️ タイマー", "⏱️ ストップウォッチ", "💤 スリープ", "📊 記録・ショップ"])

# --- 🏠 マイカフェ ---
with tab0:
    c = st.session_state.user_data["current_items"]
    bg_color = STYLE_MAP["壁"].get(c['壁'], "#f9f9f9")
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 40px; border-radius: 20px; border: 8px solid #4e342e; text-align: center;">
        <h1 style="color: #4e342e; filter: invert(0.5) grayscale(1) contrast(2);">My Study Cafe</h1>
        <div style="font-size: 100px; margin: 20px; position: relative;">
            <div style="font-size: 20px; animation: steam 2s infinite; position: absolute; left: 45%; top: -20px;">♨️</div>
            ☕ 📖
        </div>
        <p style="color: #333; font-weight: bold;">🖼️ 壁: {c['壁']} | 🪑 机: {c['テーブル']} | 🪧 看板: {c['看板']}</p>
    </div>
    <style> @keyframes steam {{ 0% {{ opacity:0; transform:translateY(0); }} 50% {{ opacity:1; }} 100% {{ opacity:0; transform:translateY(-20px); }} }} </style>
    """, unsafe_allow_html=True)
    st.info(f"💡 豆知識: {random.choice(STUDY_TRIVIA + COFFEE_TRIVIA)}")

# --- ⏲️ タイマー ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        mode = st.radio("モード", ["勉強 (25分)", "休憩 (5分)"], horizontal=True)
        t_note = st.text_input("アラーム用メモ")
    t_min = 25 if "勉強" in mode else 5
    if st.button("タイマー開始"):
        ph = st.empty()
        for t in range(t_min * 60, -1, -1):
            m, s = divmod(t, 60)
            ph.metric("残り", f"{m:02d}:{s:02d}")
            time.sleep(1)
        complete_session(mode, t_min, "勉強" in mode)
        if t_note: st.warning(f"📝 {t_note}")

# --- ⏱️ ストップウォッチ ---
with tab2:
    sw_ph = st.empty()
    c1, c2 = st.columns(2)
    if c1.button("計測開始"):
        st.session_state.sw_start = time.time()
        st.session_state.sw_running = True
    if c2.button("記録してストップ"):
        if "sw_start" in st.session_state:
            elapsed = int((time.time() - st.session_state.sw_start) // 60)
            complete_session("自由計測", elapsed, True)
            st.session_state.sw_running = False
            st.rerun()
    if st.session_state.get("sw_running", False):
        while st.session_state.sw_running:
            diff = int(time.time() - st.session_state.sw_start)
            m, s = divmod(diff, 60)
            sw_ph.metric("経過時間", f"{m:02d}:{s:02d}")
            time.sleep(1)

# --- 💤 スリープ ---
with tab3:
    s_min = st.number_input("何分後に鳴らす？", 1, 120, 60)
    s_note = st.text_input("終了メッセージ", "起きて！")
    if st.button("スリープタイマー開始"):
        ph = st.empty()
        for t in range(s_min * 60, -1, -1):
            m, s = divmod(t, 60)
            ph.metric("あと", f"{m:02d}:{s:02d}")
            time.sleep(1)
        play_alarm()
        st.error(f"⏰ {s_note}")

# --- 📊 記録・ショップ ---
with tab4:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("📚 学習履歴")
        for log in reversed(st.session_state.user_data["logs"]):
            st.caption(f"{log['date']} | {log['mode']} | {log['min']}分")
    with col_r:
        st.subheader("🛒 ショップ")
        st.write(f"所持: {st.session_state.user_data['total_beans']} 🫘")
        for cat, items in INTERIOR_SHOP.items():
            with st.expander(f"{cat}を購入"):
                for name, price in items.items():
                    owned = name in st.session_state.user_data["unlocked_items"] or name in st.session_state.user_data["unlocked_sounds"]
                    if st.button(f"{name} ({price}🫘)", disabled=owned, key=f"shop_{name}"):
                        if st.session_state.user_data["total_beans"] >= price:
                            st.session_state.user_data["total_beans"] -= price
                            if cat == "音": st.session_state.user_data["unlocked_sounds"].append(name)
                            else: st.session_state.user_data["unlocked_items"].append(name)
                            save_data(st.session_state.user_data)
                            st.rerun()
