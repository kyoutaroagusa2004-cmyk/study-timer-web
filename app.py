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

# 背景画像の読み込み（ファイル名が study.png であることを確認）
img_base64 = get_image_base64("study.png")

# HTML/CSS/JSコード
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
            width: 800px; /* 横幅を固定してズレを防止 */
        }}
        .bg-image {{ 
            width: 100%; 
            display: block; 
        }}

        /* ★スマホ画面内の配置（タイマーを大幅に右下へ移動） */
        .smartphone-screen {{ 
            position: absolute; 
            top: 28%;    /* スマホ画面の中央の高さへ */
            left: 77%;   /* 右側の白い枠の中へ */
            width: 130px;  
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        #timer {{ 
            font-family: 'Orbitron', sans-serif; 
            font-size: 24px; /* 枠に収まるサイズ */
            font-weight: bold; 
            color: #222; 
            line-height: 1;
            margin-bottom: 5px;
        }}

        .controls button {{ 
            font-size: 9px; 
            padding: 2px 6px; 
            cursor: pointer; 
        }}

        /* ★「勉強を終了する」ボタン（文字のすぐ下へ） */
        #finish-btn {{ 
            position: absolute; 
            top: 65%;    /* 「努力は...」のすぐ下に移動 */
            left: 28%;   /* 文字の中央付近へ移動 */
            padding: 8px 18px; 
            background-color: #fff; 
            border: 1px solid #ccc; 
            border-radius: 6px;
            font-size: 16px; 
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
                    alert("時間です！お疲れ様でした。");
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

# Streamlitの表示枠のサイズ
components.html(html_code, height=600, width=900)
