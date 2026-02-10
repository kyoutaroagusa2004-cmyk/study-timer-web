import streamlit as st
import streamlit.components.v1 as components
import base64

# ページの設定（タイトルとレイアウト）
st.set_page_config(page_title="勉強管理タイマー", layout="wide")

# 画像をBase64に変換して読み込む関数
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# 背景画像の読み込み（同じフォルダの study.png を探します）
img_base64 = get_image_base64("study.png")

# HTML/CSS/JSコード（デザインと動きの全貌）
html_code = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; display: flex; justify-content: center; background-color: transparent; }}
        
        /* ★全体のサイズ調節：ここの数字を変えると全体が拡大・縮小されます */
        .study-wrapper {{ 
            position: relative; 
            display: inline-block; 
            width: 900px;  /* ←ここを1000pxなどにするとサイト内で大きくなります */
        }}
        
        .bg-image {{ 
            width: 100%; 
            display: block; 
        }}

        /* スマホ画面内（タイマー）の位置：画像に合わせた最終微調整 */
        .smartphone-screen {{ 
            position: absolute; 
            top: 25.5%;    
            left: 77.5%;   
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
            margin-bottom: 4px;
        }}

        .controls {{ display: flex; gap: 5px; }}
        .controls button {{ 
            font-size: 9px; 
            padding: 2px 6px; 
            cursor: pointer; 
            border: 1px solid #ccc;
            background: #fff;
            border-radius: 3px;
        }}

        /* ★「勉強を終了する」ボタンの位置：文字のすぐ下へ */
        #finish-btn {{ 
            position: absolute; 
            top: 75%;    /* 文字「努力は...」のすぐ下に配置 */
            left: 48%;   
            transform: translateX(-50%); 
            padding: 8px 18px; 
            background-color: #fff; 
            border: 1px solid #ddd; 
            border-radius: 6px;
            font-size: 16px; 
            font-weight: bold;
            color: #444;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            white-space: nowrap;
        }}
        #finish-btn:hover {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <div class="study-wrapper">
        <!-- 背景画像の表示 -->
        <img src="data:image/png;base64,{img_base64}" class="bg-image">
        
        <!-- スマホ画面のタイマー -->
        <div class="smartphone-screen">
            <div id="timer">25:00</div>
            <div class="controls">
                <button id="start-btn">開始</button>
                <button id="stop-btn">停止</button>
            </div>
        </div>

        <!-- 終了ボタン -->
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

# Streamlit上の表示エリアのサイズ調節（画像より少し大きめに設定）
components.html(html_code, height=750, width=1100)
