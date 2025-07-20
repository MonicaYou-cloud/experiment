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

#題一
elif st.session_state.page == 2:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("高級圖形一 (1).png")
            st.image(image1, caption="練習題1")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("高級圖形一選項 (1).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["1", "2", "3", "4", "5", "6", "7", "8"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer1' not in st.session_state:
        st.session_state.show_answer1 = False
    if 'show_explanation1' not in st.session_state:
        st.session_state.show_explanation1 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer1 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation1 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer1:
        st.markdown("""
        正確答案是 **8**""")
        
    if st.session_state.show_explanation1:
        st.markdown("""
        詳解：本題中圖形的位置位於三條橫向點點線與一條直向直線
        """)

#題二
elif st.session_state.page == 3:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("高級圖形一 (2).png")
            st.image(image1, caption="練習題2")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("高級圖形一選項 (2).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["1", "2", "3", "4", "5", "6", "7", "8"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer:
        st.markdown("""
        正確答案是 **8**""")
        
    if st.session_state.show_explanation:
        st.markdown("""
        詳解：本題中圖形的位置位於三條橫向點點線與一條直向直線
        """)



# # 完成頁面
# elif st.session_state.page == 5:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
#     st.success("問卷已完成！非常感謝您的作答。")
#     st.balloons()
