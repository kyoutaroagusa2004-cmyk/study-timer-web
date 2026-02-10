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
            width: 800px; /* 表示サイズを固定してズレを防止 */
        }}
        .bg-image {{ 
            width: 100%; 
            display: block; 
        }}

        /* ★スマホ画面内の配置（タイマーを右へ、少し下へ） */
        .smartphone-screen {{ 
            position: absolute; 
            top: 15%;    /* 「Study time」より下へ下げる */
            left: 71%;   /* 右側のスマホの枠内へ移動 */
            width: 110px;  
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        #timer {{ 
            font-family: 'Orbitron', sans-serif; 
            font-size: 20px; /* スマホの枠に収まるサイズに調整 */
            font-weight: bold; 
            color: #222; 
            line-height: 1.2;
        }}

        .controls button {{ 
            font-size: 8px; 
            padding: 1px 4px; 
            cursor: pointer; 
        }}

        /* ★「勉強を終了する」ボタン（文字のすぐ下へ） */
        #finish-btn {{ 
            position: absolute; 
            top: 75%;    /* 「努力は...」のすぐ下へ */
            left: 28%;   /* ノートの中央寄りに微調整 */
            padding: 6px 12px; 
            background-color: #fff; 
            border: 1px solid #ccc; 
            border-radius: 4px;
            font-size: 16px; 
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

# 表示サイズ設定
components.html(html_code, height=600, width=900)
