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
            # 新機能用の項目がなければ追加する（アップデート対応）
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

def play_alarm():
    sound_key = st.session_state.user_data.get("current_sound", "デフォルトベル")
    sound_url = SOUND_LIBRARY.get(sound_key)
    st.components.v1.html(f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>', height=0)

# --- 4. 雑学 & 褒め言葉 ---
STUDY_TRIVIA = ["青いペンで書くと記憶力が上がる説がある", "試験直前の昼寝は記憶の整理に有効", "独り言を言いながら勉強すると効率UP"]
COFFEE_TRIVIA = ["コーヒーは元々『薬』として飲まれていた", "世界で一番高いコーヒーは象の糞から採れる", "コーヒーの香りはリラックス効果抜群"]
PRAISE_MSGS = ["天才すぎる！", "その調子！コーヒーが美味しくなるね", "努力の天才！", "集中力、神レベル！"]

# --- 5. メインUI ---
st.title("☕ Study Coffee Pro+: My Cafe")

# サイドバー: ステータスと世界時計
with st.sidebar:
    st.header("🌍 世界時計")
    now = datetime.datetime.now()
    st.write(f"🇯🇵 日本: {now.strftime('%H:%M')}")
    st.write(f"🇺🇸 NY: {(now - datetime.timedelta(hours=14)).strftime('%H:%M')}")
    
    st.divider()
    st.metric("現在の所持数", f"{st.session_state.user_data['total_beans']} 🫘 豆")
    
    st.subheader("🎵 音設定")
    selected_sound = st.selectbox("使用する音", st.session_state.user_data["unlocked_sounds"])
    if selected_sound != st.session_state.user_data["current_sound"]:
        st.session_state.user_data["current_sound"] = selected_sound
        save_data(st.session_state.user_data)

    st.subheader("🛠️ 模様替え")
    for cat in ["壁", "テーブル", "看板"]:
        options = [i for i in st.session_state.user_data["unlocked_items"] if i in INTERIOR_SHOP.get(cat, {}) or i in ["白壁", "丸太のテーブル", "なし"]]
        choice = st.selectbox(f"{cat}", options, key=f"select_{cat}")
        st.session_state.user_data["current_items"][cat] = choice

# --- 6. タブ機能 ---
tab0, tab1, tab2, tab3, tab4 = st.tabs(["🏠 マイカフェ", "⏲️ タイマー", "💤 スリープ", "🛒 ショップ", "📊 記録"])

# タブ0: マイカフェ表示
with tab0:
    c = st.session_state.user_data["current_items"]
    st.markdown(f"""
    <div style="border: 5px solid #4e342e; padding: 30px; border-radius: 15px; background-color: #fdf5e6; text-align: center;">
        <h1 style="color: #4e342e;">🏠 Your Cafe</h1>
        <p>🖼️ 壁: {c['壁']} | 🪑 机: {c['テーブル']} | 🪧 看板: {c['看板']}</p>
        <div style="font-size: 80px; margin: 20px;">
            {"🧱" if "レンガ" in c['壁'] else "🌲" if "木目" in c['壁'] else "✨" if "星空" in c['壁'] else "⬜"}
            ☕ 📖
            {"🛋️" if "アンティーク" in c['テーブル'] else "🪵" if "丸太" in c['テーブル'] else "🖥️"}
        </div>
    </div>
    """, unsafe_allow_html=True)

# タブ1: タイマー
with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        mode = st.radio("モード", ["勉強 (25分)", "休憩 (5分)"], horizontal=True)
        note = st.text_input("終了時のメモ（アラームと一緒に表示）")
    
    study_time = 25 if "勉強" in mode else 5
    if st.button("タイマー開始"):
        ph = st.empty()
        st.info(f"💡 {random.choice(STUDY_TRIVIA if '勉強' in mode else COFFEE_TRIVIA)}")
        for t in range(study_time * 60, -1, -1):
            m, s = divmod(t, 60)
            ph.metric("残り時間", f"{m:02d}:{s:02d}")
            time.sleep(1)
        # 終了処理
        beans = study_time // 10 if "勉強" in mode else 0
        st.session_state.user_data["total_beans"] += beans
        st.session_state.user_data["logs"].append({"date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), "mode": mode, "min": study_time})
        save_data(st.session_state.user_data)
        play_alarm()
        st.balloons() if "勉強" in mode else st.snow()
        st.success(f"{random.choice(PRAISE_MSGS)} {beans}粒獲得！ {f'📝:{note}' if note else ''}")

# タブ2: スリープタイマー
with tab3:
    s_min = st.number_input("アラーム設定（分）", 1, 120, 60)
    s_note = st.text_input("アラームメッセージ", "時間だよ！起きて！")
    if st.button("スリープ開始"):
        ph = st.empty()
        for t in range(s_min * 60, -1, -1):
            m, s = divmod(t, 60)
            ph.metric("アラームまで", f"{m:02d}:{s:02d}")
            time.sleep(1)
        play_alarm()
        st.error(f"⏰ {s_note}")

# タブ3: ショップ
with tab4:
    st.subheader("🛒 ショップ")
    for cat, items in INTERIOR_SHOP.items():
        st.write(f"### {cat}")
        cols = st.columns(3)
        for i, (name, price) in enumerate(items.items()):
            with cols[i % 3]:
                is_owned = name in st.session_state.user_data["unlocked_items"] or name in st.session_state.user_data["unlocked_sounds"]
                if st.button(f"{name} ({price}🫘)", disabled=is_owned, key=f"buy_{name}"):
                    if st.session_state.user_data["total_beans"] >= price:
                        st.session_state.user_data["total_beans"] -= price
                        if cat == "音": st.session_state.user_data["unlocked_sounds"].append(name)
                        else: st.session_state.user_data["unlocked_items"].append(name)
                        save_data(st.session_state.user_data)
                        st.rerun()
                    else: st.error("豆が足りないよ！")

# タブ4: 記録
with tab2:
    st.subheader("📊 記録")
    for log in reversed(st.session_state.user_data["logs"]):
        st.text(f"📅 {log['date']} | {log['mode']} | {log['min']}分")
