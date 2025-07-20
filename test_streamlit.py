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
    st.session_state.page = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# 換頁函式
def next_page():
    st.session_state.page += 1
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

def prev_page():
    st.session_state.page -= 1

# 顯示計時器
if st.session_state.page > 0 and st.session_state.start_time:
    elapsed_seconds = int(time.time() - st.session_state.start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    st.markdown(f"⏱️ **測驗時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 歡迎頁
if st.session_state.page == 0:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.title("📝 歡迎參加測驗")
    st.write("本測驗包含數題圖片與選項，請專心作答。")
    st.button("👉 開始測驗", on_click=next_page)

# 頁 1：基本資料與題組 1
elif st.session_state.page == 1:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.header("基本資料")
    st.write("請填寫以下問卷，完成後按下一頁。")

    age = st.radio("請問您是否為大專院校的學生？", ["是", "否"])
    gender = st.radio("請選擇您的性別", ["男", "女", "其他"])
    st.button("下一頁", on_click=next_page)

elif st.session_state.page == 2:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.header("練習題")
    
    try:
    image1 = Image.open("高級圖形一 (1).png")
    st.image(image1, caption="請從以下選項選擇您認為的正確答案")
    image2 = Image.open("高級圖形一選項 (1).png")
    st.image(image2, caption="選項")
    except FileNotFoundError:
    st.warning("⚠️ 無法載入圖片，請確認檔案名稱與路徑正確。")
    
    st.button("上一頁", on_click=prev_page)
    st.button("下一頁", on_click=next_page)

# 頁 2：題組 2
elif st.session_state.page == 3:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.header("練習題")
    st.radio("2. 你喜歡咖啡還是茶？", ["咖啡", "茶"], key="q2_1")
    st.button("上一頁", on_click=prev_page)
    st.button("下一頁", on_click=next_page)

# 頁 3：題組 3
elif st.session_state.page == 4:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.header("練習題")
    st.radio("3. 請選擇您覺得正確的選項？", ["1", "2"], key="q3_1")
    st.button("上一頁", on_click=prev_page)
    st.button("提交", on_click=next_page)

# 完成頁面
elif st.session_state.page == 5:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.success("問卷已完成！非常感謝您的作答。")
    st.balloons()
