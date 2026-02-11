import streamlit as st
import time
import datetime

# --- セッション状態の管理 ---
if 'pomo_stage' not in st.session_state:
    st.session_state.pomo_stage = "集中" # "集中", "入力", "休憩" の3段階
if 'running' not in st.session_state:
    st.session_state.running = False

st.title("☕ Study Coffee")

# --- メインロジック ---
placeholder = st.empty() # タイマー表示用

if st.session_state.pomo_stage == "集中":
    st.subheader("🖋️ 今は集中する時間です")
    
    # タイマー本体
    if st.session_state.running:
        for t in range(25 * 60, -1, -1):
            if not st.session_state.running: break
            mins, secs = divmod(t, 60)
            placeholder.metric("残り時間", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        
        if t <= 0:
            st.session_state.pomo_stage = "入力"
            st.session_state.running = False
            st.rerun()
    else:
        placeholder.metric("集中タイマー", "25:00")
        if st.button("25分タイマーを開始する", use_container_width=True):
            st.session_state.running = True
            st.rerun()

elif st.session_state.pomo_stage == "入力":
    st.subheader("✅ お疲れ様！何をしたかメモしよう")
    study_note = st.text_input("勉強した内容を入力してください（例：数学のワーク3ページ）")
    
    if st.button("記録して休憩に入る", use_container_width=True):
        if study_note:
            # ログに保存
            with open("study_log.csv", "a", encoding="utf-8") as f:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                f.write(f"{now},集中,25,{study_note}\n")
            
            st.session_state.pomo_stage = "休憩"
            st.rerun()
        else:
            st.warning("内容を入力してください！")

elif st.session_state.pomo_stage == "休憩":
    st.subheader("☕ 休憩タイム（5分）")
    
    if st.session_state.running:
        for t in range(5 * 60, -1, -1):
            if not st.session_state.running: break
            mins, secs = divmod(t, 60)
            placeholder.metric("休憩の残り", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            
        if t <= 0:
            st.balloons()
            st.success("休憩終了！次の25分を始めましょう。")
            st.session_state.pomo_stage = "集中"
            st.session_state.running = False
            time.sleep(2)
            st.rerun()
    else:
        placeholder.metric("休憩タイマー", "05:00")
        if st.button("5分の休憩を始める", use_container_width=True):
            st.session_state.running = True
            st.rerun()

# 勉強を終了するボタン
if st.button("勉強を終了する", type="secondary"):
    st.session_state.pomo_stage = "集中"
    st.session_state.running = False
    st.write("今日もお疲れ様でした！")
