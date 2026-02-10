import streamlit as st
import streamlit.components.v1 as components
import base64

# ページの設定（横幅を広くする）
st.set_page_config(layout="wide")

# 画像をBase64に変換して読み込む関数
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 背景画像の読み込み
img_base64 = get_image_base64("study.png")

# HTML/CSS/JSコード（これまでの完成版）
# st.codeなどで表示するのではなく、HTMLとして埋め込みます
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com" rel="stylesheet">
    <style>
        .study-wrapper {{ position: relative; display: inline-block; }}
        .bg-image {{ width: 1000px; }}
        .smartphone-screen {{ 
            position: absolute; 
            top: 148px; 
            left: 765px; 
            width: 140px; 
            text-align: center; 
        }}
        #timer {{ 
            font-family: 'Orbitron', sans-serif; 
            font-size: 32px; 
            font-weight: bold; 
            color: #333; 
            margin-bottom: 5px;
        }}
        #stopwatch {{ font-size: 12px; color: #555; margin-bottom: 5px; }}
        #finish-btn {{ 
            position: absolute; 
            top: 410px; 
            left: 330px; 
            padding: 8px 16px; 
            background-color: #fff; 
            border: 1px solid #ccc; 
            border-radius: 5px;
            font-size: 24px; 
            cursor: pointer;
        }}
        .controls button {{ font-size: 10px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="study-wrapper">
        <img src="data:image/png;base64,{img_base64}" class="bg-image">
        <div class="smartphone-screen">
            <div id="stopwatch">Total 00:00</div>
            <div id="timer">25:00</div>
            <div class="controls">
                <button id="start-btn">開始</button>
                <button id="stop-btn">停止</button>
            </div>
        </div>
        <button id="finish-btn">勉強を終了する</button>
    </div>
    <script>
        let timeLeft = 25 * 60;
        let totalSeconds = 0;
        let timerId = null;
        const timerDisplay = document.getElementById('timer');
        const stopwatchDisplay = document.getElementById('stopwatch');
        function updateDisplay() {{
            let m = Math.floor(timeLeft / 60);
            let s = timeLeft % 60;
            timerDisplay.innerText = `${{m.toString().padStart(2, '0')}}:${{s.toString().padStart(2, '0')}}`;
            let sm = Math.floor(totalSeconds / 60);
            let ss = totalSeconds % 60;
            stopwatchDisplay.innerText = `Total ${{sm.toString().padStart(2, '0')}}:${{ss.toString().padStart(2, '0')}}`;
        }}
        document.getElementById('start-btn').addEventListener('click', () => {{
            if (timerId !== null) return;
            timerId = setInterval(() => {{
                if (timeLeft > 0) timeLeft--;
                totalSeconds++;
                updateDisplay();
            }}, 1000);
        }});
        document.getElementById('stop-btn').addEventListener('click', () => {{
            clearInterval(timerId);
            timerId = null;
        }});
        document.getElementById('finish-btn').addEventListener('click', () => {{
            clearInterval(timerId);
            alert(`お疲れ様でした！勉強時間は ${{Math.floor(totalSeconds / 60)}} 分です。`);
            location.reload();
        }});
    </script>
</body>
</html>
"""

# Streamlitに表示（サイズは画像に合わせて調整）
components.html(html_code, height=800, width=1100)
