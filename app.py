import streamlit as st
import streamlit.components.v1 as components
import base64

# ページの設定（横幅を広くし、タイトルを設定）
st.set_page_config(page_title="勉強管理タイマー", layout="wide")

# 画像をBase64に変換して読み込む関数
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# 背景画像の読み込み（ファイル名が study.png であることを確認してください）
img_base64 = get_image_base64("study.png")

# HTML/CSS/JSコード
html_code = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background-color: transparent; }}
        .study-wrapper {{ 
            position: relative; 
            display: inline-block; 
            width: 1000px;
            margin: 0 auto;
        }}
        .bg-image {{ 
            width: 100%; 
            display: block; 
        }}

        /* ★スマホ画面内の配置（タイマーを大幅に上に移動） */
        .smartphone-screen {{ 
            position: absolute; 
            top: 45px;    /* 画像に合わせて大幅に引き上げ */
            left: 768px;   
            width: 130px;  
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        #stopwatch {{ 
            font-size: 11px; 
            color: #333; 
            margin-bottom: 2px;
            font-family: sans-serif;
        }}

        #timer {{ 
            font-family: 'Orbitron', sans-serif; 
            font-size: 28px; 
            font-weight: bold; 
            color: #222; 
            margin-bottom: 5px;
            line-height: 1;
        }}

        .controls {{ display: flex; gap: 4px; }}
        .controls button {{ 
            font-size: 9px; 
            padding: 2px 6px; 
            cursor: pointer; 
            border: 1px solid #ccc;
            border-radius: 3px;
            background: #fff;
        }}

        /* ★「勉強を終了する」ボタン（文字の下へ移動） */
        #finish-btn {{ 
            position: absolute; 
            top: 605px;    /* 「努力は...」の文字のすぐ下へ */
            left: 335px;   /* ノートの中央付近 */
            padding: 10px 24px; 
            background-color: #ffffff; 
            border: 1px solid #dcdcdc; 
            border-radius: 8px;
            font-size: 18px; 
            font-weight: bold;
            color: #444;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: 0.2s;
        }}
        #finish-btn:hover {{ background-color: #f8f8f8; }}
    </style>
</head>
<body>
    <div class="study-wrapper">
        <!-- 画像が表示されない場合はBase64をチェック -->
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
        const startBtn = document.getElementById('start-btn');
        const stopBtn = document.getElementById('stop-btn');

        function updateDisplay() {{
            let m = Math.floor(timeLeft / 60);
            let s = timeLeft % 60;
            timerDisplay.innerText = `${{m.toString().padStart(2, '0')}}:${{s.toString().padStart(2, '0')}}`;

            let sm = Math.floor(totalSeconds / 60);
            let ss = totalSeconds % 60;
            stopwatchDisplay.innerText = `Total ${{sm.toString().padStart(2, '0')}}:${{ss.toString().padStart(2, '0')}}`;
        }}

        startBtn.addEventListener('click', () => {{
            if (timerId !== null) return;
            timerId = setInterval(() => {{
                if (timeLeft > 0) timeLeft--;
                totalSeconds++;
                updateDisplay();
            }}, 1000);
        }});

        stopBtn.addEventListener('click', () => {{
            clearInterval(timerId);
            timerId = null;
        }});

        document.getElementById('finish-btn').addEventListener('click', () => {{
            clearInterval(timerId);
            const finalMin = Math.floor(totalSeconds / 60);
            const finalSec = totalSeconds % 60;
            alert(`お疲れ様でした！今回の勉強時間は ${{finalMin}}分${{finalSec}}秒 です。`);
            location.reload();
        }});
    </script>
</body>
</html>
"""

# Streamlitの画面に埋め込み（height, widthは画像のサイズに合わせています）
components.html(html_code, height=800, width=1050)
