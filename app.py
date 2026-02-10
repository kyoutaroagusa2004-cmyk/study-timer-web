import streamlit as st
import streamlit.components.v1 as components
import base64

# ページの設定
st.set_page_config(page_title="勉強管理タイマー", layout="wide")

# 画像をBase64に変換して読み込む関数
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# 背景画像の読み込み
img_base64 = get_image_base64("study.png")

# HTML/CSS/JSコード
html_code = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; background-color: transparent; }}
        .study-wrapper {{ 
            position: relative; 
            display: inline-block; 
            width: 800px; /* 画像の表示サイズに合わせて調整 */
        }}
        .bg-image {{ 
            width: 100%; 
            display: block; 
        }}

        /* ★タイマー（スマホの画面内）の位置調整 */
        .smartphone-screen {{ 
            position: absolute; 
            top: 22%;    /* ％指定にしてズレを防止 */
            left: 54%;   
            width: 140px;  
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        #timer {{ 
            font-family: 'Orbitron', sans-serif; 
            font-size: 28px; 
            font-weight: bold; 
            color: #222; 
            line-height: 1;
            margin-bottom: 5px;
        }}

        .controls button {{ 
            font-size: 10px; 
            padding: 2px 8px; 
            cursor: pointer; 
        }}

        /* ★「勉強を終了する」ボタン（文字の真下へ） */
        #finish-btn {{ 
            position: absolute; 
            top: 70%;    /* 「努力は...」のすぐ下の位置 */
            left: 33%;   
            padding: 8px 16px; 
            background-color: #fff; 
            border: 1px solid #ccc; 
            border-radius: 5px;
            font-size: 18px; 
            font-weight: bold;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="study-wrapper">
        <img src="data:image/png;base64,{img_base64}" class="bg-image">
        
        <div class="smartphone-screen">
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
        let timerId = null;
        const timerDisplay = document.getElementById('timer');

        function updateDisplay() {{
            let m = Math.floor(timeLeft / 60);
            let s = timeLeft % 60;
            timerDisplay.innerText = `${{m.toString().padStart(2, '0')}}:${{s.toString().padStart(2, '0')}}`;
        }}

        document.getElementById('start-btn').addEventListener('click', () => {{
            if (timerId !== null) return;
            timerId = setInterval(() => {{
                if (timeLeft > 0) timeLeft--;
                updateDisplay();
                if (timeLeft <= 0) {{
                    clearInterval(timerId);
                    alert("お疲れ様でした！");
                }}
            }}, 1000);
        }});

        document.getElementById('stop-btn').addEventListener('click', () => {{
            clearInterval(timerId);
            timerId = null;
        }});

        document.getElementById('finish-btn').addEventListener('click', () => {{
            location.reload();
        }});
    </script>
</body>
</html>
"""

# Streamlitの表示サイズ設定
components.html(html_code, height=600, width=900)
