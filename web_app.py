import streamlit as st
import time
import datetime
import os
import random

# ページ設定
st.set_page_config(page_title="Study Coffee", page_icon="☕")

# --- 雑学データ ---
STUDY_TRIVIA = [
    "西郷隆盛の有名な肖像画は、実は本人ではなく親戚をモデルに描かれたもの",
    "世界で最も多い名前は「ムハンマド」と言われている",
    "人の大腿骨は、実はコンクリートよりも硬い",
    "学校の黒板の値段は、1枚あたり約13万円ほど",
    "赤ちゃんの骨は約300個あるが、大人になると206個に減る"
]

COFFEE_TRIVIA = [
    "コーヒーは「豆」ではなく、コーヒーチェリーという果実の「種」",
    "コーヒーは世界で水の次に多く飲まれている飲み物",
    "コーヒーの記録は900年頃、医師が「薬」として使ったのが最初",
    "コーヒーの粉には脱臭効果があり、冷蔵庫や靴箱の消臭に使える",
    "18世紀のドイツでは、通貨の流出を防ぐためにコーヒー禁止令が出たことがある"
]

# --- セッション状態の初期化 ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'stopwatch_running' not in st.session_state:
    st.session_state.stopwatch_running = False

# --- 関数: 記録と豆の計算 ---
def save_log(mode, minutes):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    with open("study_log.csv", "a", encoding="utf-8") as f:
        f.write(f"{now},{mode},{minutes}\n")

def get_total_beans():
    if not os.path.exists("study_log.csv"):
        return 0
    total_min = 0
    with open("study_log.csv", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3 and ("勉強" in parts[1] or "ストップウォッチ" in parts[1]):
                total_min += int(parts[2])
    return total_min // 10  # 10分で1粒

# --- メインUI ---
st.title("☕ Study Coffee (Beta)")

# 常に現在の豆の数を表示
current_beans = get_total_beans()
st.sidebar.metric("現在の所持数", f"{current_beans} 🫘 豆")
st.sidebar.info("10分勉強するごとに1粒貯まります！")

tab1, tab2, tab3 = st.tabs(["⏲️ ポモドーロ", "⏱️ ストップウォッチ", "📊 記録・ショップ"])

# --- Tab 1: ポモドーロタイマー ---
with tab1:
    st.subheader("集中と休憩のサイクル")
    mode = st.radio("モード選択", ["勉強 (25分)", "休憩 (5分)"], horizontal=True)
    study_time = 25 if "勉強" in mode else 5
    
    col1, col2 = st.columns(2)
    if col1.button("タイマー開始", key="pomo_start", use_container_width=True):
        st.session_state.running = True
    if col2.button("リセット", key="pomo_reset", use_container_width=True):
        st.session_state.running = False
        st.rerun()

    placeholder = st.empty()
    trivia_placeholder = st.empty() # 雑学用

    if st.session_state.running:
        # タイマー開始時にランダムに雑学を選択
        trivia_text = random.choice(STUDY_TRIVIA if "勉強" in mode else COFFEE_TRIVIA)
        trivia_placeholder.info(f"💡 **豆知識:** {trivia_text}")
        
        for t in range(study_time * 60, -1, -1):
            if not st.session_state.running: break
            mins, secs = divmod(t, 60)
            placeholder.metric("残り時間", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        
        if t <= 0:
            save_log(mode, study_time)
            st.balloons() if "勉強" in mode else st.snow()
            st.success(f"{mode}完了！ {study_time // 10 if '勉強' in mode else 0} 粒の豆を獲得しました。")
            st.session_state.running = False
            st.rerun()

# --- Tab 2: ストップウォッチ ---
with tab2:
    st.subheader("自由計測")
    sw_placeholder = st.empty()
    sw_trivia_placeholder = st.empty()
    c1, c2 = st.columns(2)
    
    if c1.button("計測開始", key="sw_start", use_container_width=True):
        st.session_state.stopwatch_running = True
        st.session_state.start_time = time.time()

    if c2.button("ストップ & 記録", key="sw_stop", use_container_width=True):
        if st.session_state.stopwatch_running:
            elapsed = int((time.time() - st.session_state.start_time) // 60)
            save_log("ストップウォッチ", elapsed)
            st.session_state.stopwatch_running = False
            st.success(f"{elapsed}分勉強しました！ {elapsed // 10} 粒の豆を獲得！")
            st.rerun()

    if st.session_state.stopwatch_running:
        sw_trivia_placeholder.info(f"💡 **勉強の雑学:** {random.choice(STUDY_TRIVIA)}")
        while st.session_state.stopwatch_running:
            elapsed_sec = int(time.time() - st.session_state.start_time)
            mins, secs = divmod(elapsed_sec, 60)
            sw_placeholder.metric("経過時間", f"{mins:02d}:{secs:02d}")
            time.sleep(1)

# --- Tab 3: 記録・ショップ ---
with tab3:
    st.subheader("📚 学習履歴")
    if os.path.exists("study_log.csv"):
        with open("study_log.csv", "r", encoding="utf-8") as f:
            logs = f.readlines()
            total_min = 0
            for log in reversed(logs):
                parts = log.strip().split(',')
                if len(parts) == 3:
                    st.text(f"📅 {parts[0]} | {parts[1]} | {parts[2]}分")
                    if "勉強" in parts[1] or "ストップウォッチ" in parts[1]:
                        total_min += int(parts[2])
            
            st.divider()
            st.metric("合計勉強時間", f"{total_min} 分")
            st.metric("現在のコーヒー豆", f"{current_beans} 粒 🫘")
    else:
        st.write("まだ記録がありません。")

    st.divider()
    st.subheader("🛒 コーヒーショップ (Coming Soon)")
    st.write(f"現在 **{current_beans} 粒** の豆を持っています。")
    st.button("高級豆と交換 (100粒)", disabled=True)
