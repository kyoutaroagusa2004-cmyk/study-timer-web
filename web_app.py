import streamlit as st
import time
import datetime
import os
import json

# --- 1. ページ設定 ---
st.set_page_config(page_title="Study Coffee Pro+", page_icon="☕", layout="wide")

# --- 2. データの読み込みと保存 ---
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            defaults = {
                "total_beans": 0, "logs": [], "cafe_name": "My Coffee",
                "unlocked_items": ["白壁", "丸太のテーブル"], 
                "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁"},
                "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル"
            }
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
    return {
        "total_beans": 0, "logs": [], "cafe_name": "My Coffee",
        "unlocked_items": ["白壁", "丸太のテーブル"], 
        "current_items": {"テーブル": "丸太のテーブル", "壁紙": "白壁"},
        "unlocked_sounds": ["デフォルトベル"], "current_sound": "デフォルトベル"
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

# --- 3. ビジュアル素材（確実に表示される画像URL） ---
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

# --- 4. サイドバー ---
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
        unlocked = st.session_state.user_data["unlocked_items"]
        default_val = "白壁" if cat == "壁紙" else "丸太のテーブル"
        options = [k for k in (WALLPAPER_MAP if cat=="壁紙" else TABLE_MAP).keys() if k in unlocked or k == default_val]
        current = st.session_state.user_data["current_items"].get(cat, default_val)
        idx = options.index(current) if current in options else 0
        st.session_state.user_data["current_items"][cat] = st.selectbox(f"{cat}を選択", options, index=idx, key=f"select_{cat}")
    
    st.session_state.user_data["current_sound"] = st.selectbox("アラーム音", st.session_state.user_data["unlocked_sounds"])

    if st.button("設定を保存して更新", use_container_width=True):
        save_data(st.session_state.user_data)
        st.rerun()

# --- 5. メイン画面描画 (CSS) ---
current_bg = WALLPAPER_MAP.get(st.session_state.user_data["current_items"].get("壁紙", "白壁"))
current_tbl = TABLE_MAP.get(st.session_state.user_data["current_items"].get("テーブル", "丸太のテーブル"))

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{current_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .cafe-container {{
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 20px auto;
        max-width: 800px;
    }}
    .table-view {{
        background-image: url("{current_tbl}");
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 300px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
    }}
    </style>
    <div class="cafe-container">
        <h1 style="font-size: 3rem;">{st.session_state.user_data["cafe_name"]}</h1>
        <div class="table-view"></div>
        <p style="font-size: 24px; color: #f1c40f;">☕ Studying...</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. タブ機能 ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⏲️ Timer", "⏱️ Watch", "💤 Sleep", "🛒 Shop", "📊 Log"])

def play_alarm():
    sound_url = SOUND_LIBRARY.get(st.session_state.user_data.get("current_sound", "デフォルトベル"))
    st.components.v1.html(f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>', height=0)

with tab1: # タイマー
    if st.button("25分タイマー開始", use_container_width=True):
        ph = st.empty()
        for t in range(25 * 60, -1, -1):
            mm, ss = divmod(t, 60)
            ph.metric("Remaining", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        st.session_state.user_data["total_beans"] += 5
        st.session_state.user_data["logs"].append({"date": datetime.datetime.now().strftime('%m/%d %H:%M'), "mode": "勉強", "min": 25})
        save_data(st.session_state.user_data)
        play_alarm()
        st.balloons()
        st.rerun()

with tab4: # ショップ
    st.subheader(f"🛒 ショップ (所持: {st.session_state.user_data['total_beans']} 🫘)")
    cols = st.columns(3)
    for i, (cat, items_dict) in enumerate(INTERIOR_SHOP.items()):
        with cols[i % 3]:
            st.markdown(f"### {cat}")
            for item_name, price in items_dict.items():
                is_unlocked = item_name in st.session_state.user_data["unlocked_items"] or item_name in st.session_state.user_data["unlocked_sounds"]
                if is_unlocked:
                    st.button(f"✅ {item_name}", disabled=True, key=f"shop_{item_name}")
                elif st.button(f"{item_name} ({price} 🫘)", key=f"buy_{item_name}"):
                    if st.session_state.user_data["total_beans"] >= price:
                        st.session_state.user_data["total_beans"] -= price
                        target = "unlocked_sounds" if cat == "音" else "unlocked_items"
                        st.session_state.user_data[target].append(item_name)
                        save_data(st.session_state.user_data)
                        st.rerun()
                    else:
                        st.error("豆が足りません")

with tab5: # ログ
    if st.session_state.user_data["logs"]:
        import pandas as pd
        st.table(pd.DataFrame(st.session_state.user_data["logs"]).tail(5))
    else:
        st.write("記録はありません")
