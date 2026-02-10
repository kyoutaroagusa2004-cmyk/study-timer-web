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

# 背景画像の読み込み（同じフォルダに study.png を置いてください）
img_base64 = get_image_base64("study.png")

# HTML/CSS/JSコード（配置を最新画像に合わせて微調整済み）
html_code = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; display: flex; justify-content: center; background-color: transparent; }}
        
        .study-wrapper {{ 
            position: relative; 
            display: inline-block; 
            width: 1000px; /* ここを変えると全体の大きさを調節できます */
        }}
        
        .bg-image {{ 
            width: 100%; 
            display: block; 
        }}

        /* ★スマホ画面内のタイマー位置調整 */
        .smartphone-screen {{ 
            position: absolute; 
            top: 26%;    /* スマホの白い画面の高さへ */
            left: 77.5%;   /* 右側のスマホ画面内へ移動 */
            width: 130px;  
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        #timer {{ 
            font-family: 'Orbitron', sans-serif; 
            font-size: 26px; 
            font-weight: bold; 
            color: #222; 
            line-height: 1;
            margin-bottom: 5px;
        }}

        .controls {{ display: flex; gap: 5px; }}
        .controls button {{ 
            font-size: 9px; 
            padding: 1px 6px; 
            cursor: pointer; 
            border: 1px solid #ccc;
            background: #fff;
            border-radius: 3px;
        }}

        /* ★「勉強を終了する」ボタンの位置調整 */
        #finish-btn {{ 
            position: absolute; 
            top: 74%;    /* 文字「努力は...」のすぐ下に配置 */
            left: 48%;   
            transform: translateX(-50%); 
            padding: 6px 16px; 
            background-color: #fff; 
            border: 1px solid #ddd; 
            border-radius: 5px;
            font-size: 15px; 
            font-weight: bold;
            color: #444;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            white-space: nowrap;
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

# Streamlit上の表示エリアサイズ（全体のサイズに合わせて調整）
components.html(html_code, height=750, width=1050)
