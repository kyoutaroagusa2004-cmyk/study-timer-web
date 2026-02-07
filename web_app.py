import streamlit as st
import time
import datetime

st.set_page_config(page_title="勉強管理Webアプリ", page_icon="⏰")

st.title("⏰ 勉強管理タイマー")

# モード管理
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

col1, col2 = st.columns(2)

with col1:
    if st.button("勉強開始！"):
        st.session_state.start_time = time.time()
        st.success("計測を開始しました")

with col2:
    if st.button("終了して記録"):
        if st.session_state.start_time:
            end_time = time.time()
            duration = round((end_time - st.session_state.start_time) / 60, 1)
            
            # 学習内容入力
            note = st.text_input("何を勉強しましたか？")
            if st.button("この内容で保存"):
                with open("study_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.datetime.now()}] {duration}分: {note}\n")
                st.balloons() # お祝いの風船を飛ばす
                st.session_state.start_time = None
        else:
            st.warning("先に開始ボタンを押してください")

# 記録の表示
st.subheader("📚 今日の学習記録")
try:
    with open("study_log.txt", "r", encoding="utf-8") as f:
        st.text(f.read())
except FileNotFoundError:
    st.write("まだ記録がありません。")
