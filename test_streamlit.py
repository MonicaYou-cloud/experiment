import streamlit as st
import pandas as pd
import time
from PIL import Image

# 插入 CSS 樣式
st.markdown("""
<style>
/* 全域文字設定 */
html, body, [class*="css"]  {
    font-family: "Microsoft JhengHei", "Arial", sans-serif;
    font-size: 20px;
    line-height: 1.8;
}

/* 所有標題置中 */
h1, h2, h3, h4 {
    text-align: center;
    color: #2c3e50;
}

/* Radio 題目與選項加大 */
div[data-baseweb="radio"] {
    font-size: 20px;
}

/* 所有按鈕加大字體與寬度 */
button[kind="primary"] {
    font-size: 18px;
    padding: 0.5em 2em;
}

/* 增加輸入欄位的字體大小 */
input, textarea {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# 初始化狀態
if 'page' not in st.session_state:
    st.session_state.page = 0  # 0 是歡迎頁
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# 換頁函式（設定開始計時）
def next_page():
    st.session_state.page += 1
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

def prev_page():
    st.session_state.page -= 1

# 顯示計時器（從第 1 頁開始才顯示）
if st.session_state.start_time and st.session_state.page > 0:
    elapsed_seconds = int(time.time() - st.session_state.start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    time_str = f"{minutes:02d} 分 {seconds:02d} 秒"

    st.markdown(f"""
        <div style='position:fixed; top:20px; left:30px; background:#f0f0f0;
                    padding:8px 16px; border-radius:8px; font-size:18px;
                    box-shadow:0 0 5px rgba(0,0,0,0.1); z-index:1000;'>
            ⏱️ 測驗時間：<strong>{time_str}</strong>
        </div>
    """, unsafe_allow_html=True)

# 頁面內容根據頁數切換
if st.session_state.page == 0:
    st.title("📝 歡迎參加測驗")
    st.write("本測驗包含數題圖片與選項，請專心作答。")
    st.button("👉 開始測驗", on_click=next_page)

elif st.session_state.page == 1:
    st.header("基本資料")
    st.write("請填寫以下問卷，完成後按下一頁。")

    age = st.number_input("請輸入您的年齡", min_value=10, max_value=100, step=1)
    gender = st.radio("請選擇您的性別", ["男", "女", "其他"])

    st.title("題組 1")
    st.markdown('<div class="question-text">問題 1：你喜歡貓還是狗？</div>', unsafe_allow_html=True)
    st.radio("", ["貓", "狗"], key="q1")
    st.radio("問題 2：你喜歡早上還是晚上？", ["早上", "晚上"], key="q1_2")

    # 插入圖片題目
    try:
        image1 = Image.open("螢幕擷取畫面 2025-07-03 115532.png")
        st.image(image1, caption="題目1")
    except FileNotFoundError:
        st.warning("⚠️ 無法載入圖片，請確認圖片檔案名稱與路徑是否正確。")

    st.button("下一頁", on_click=next_page)

elif st.session_state.page == 2:
    st.title("題組 2")
    st.write("這是第二組題目")
    st.radio("問題 1：你喜歡咖啡還是茶？", ["咖啡", "茶"], key="q2_1")
    st.radio("問題 2：你喜歡夏天還是冬天？", ["夏天", "冬天"], key="q2_2")
    st.button("上一頁", on_click=prev_page)
    st.button("下一頁", on_click=next_page)

elif st.session_state.page == 3:
    st.title("題組 3")
    st.write("這是第三組題目")
    st.radio("問題 1：請選擇您覺得正確的選項？", ["1", "2"], key="q3_1")
    st.radio("問題 2：請選擇您覺得正確的選項？", ["1", "2"], key="q3_2")
    st.button("上一頁", on_click=prev_page)
    st.button("提交", on_click=next_page)

elif st.session_state.page == 4:
    st.success("問卷已完成！非常感謝您的作答 🙏")
    st.balloons()
