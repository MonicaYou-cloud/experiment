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

# 基本資料頁
elif st.session_state.page == 1:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.header("基本資料")
    st.write("請填寫以下問卷，完成後按下一頁。")

    age = st.radio("請問您是否為大專院校的學生？", ["是", "否"])
    gender = st.radio("請選擇您的性別", ["男", "女", "其他"])
    st.button("下一頁", on_click=next_page)

# 題一
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
        詳解：本題中圖形的位置位於三條橫向點點線與一條直向直線處。
        """)

# 題二
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
    if 'show_answer2' not in st.session_state:
        st.session_state.show_answer2 = False
    if 'show_explanation2' not in st.session_state:
        st.session_state.show_explanation2 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer2 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation2 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer2:
        st.markdown("""
        正確答案是 **4**""")
        
    if st.session_state.show_explanation2:
        st.markdown("""
        詳解：本題中圖形的位置位於一條橫向白線與一條直向白線，橫直白線的交會處皆會塗黑。
        """)

# 題三
elif st.session_state.page == 4:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("高級圖形二 (1).png")
            st.image(image1, caption="練習題3")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("高級圖形二選項 (1).png")
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
    if 'show_answer3' not in st.session_state:
        st.session_state.show_answer3 = False
    if 'show_explanation3' not in st.session_state:
        st.session_state.show_explanation3 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer3 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation3 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer3:
        st.markdown("""
        正確答案是 **1**""")
        
    if st.session_state.show_explanation3:
        st.markdown("""
        詳解：每一直排或每一橫排只會出現一次橫的與直的黑、白、斜線。
        """)

# 題四
elif st.session_state.page == 5:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("高級圖形二 (2).png")
            st.image(image1, caption="練習題4")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("高級圖形二選項 (2).png")
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
    if 'show_answer4' not in st.session_state:
        st.session_state.show_answer4 = False
    if 'show_explanation4' not in st.session_state:
        st.session_state.show_explanation4 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer4 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation4 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer4:
        st.markdown("""
        正確答案是 **8**""")
        
    if st.session_state.show_explanation4:
        st.markdown("""
        詳解：以橫向來看，第一張圖加上第二張圖會等於第三張，直向來看也是如此。
        """)

# 題五
elif st.session_state.page == 6:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("區分 (1).png")
            st.image(image1, caption="練習題5")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("區分選項 (1).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["A", "B", "C", "D", "E"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer5' not in st.session_state:
        st.session_state.show_answer5 = False
    if 'show_explanation5' not in st.session_state:
        st.session_state.show_explanation5 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer5 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation5 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer5:
        st.markdown("""
        正確答案是 **E**""")
        
    if st.session_state.show_explanation5:
        st.markdown("""
        詳解：箭頭以凹凸間隔，三角形以順時針轉動。
        """)

# 題六
elif st.session_state.page == 7:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("區分 (2).png")
            st.image(image1, caption="練習題6")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("區分選項 (2).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["A", "B", "C", "D", "E"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer6' not in st.session_state:
        st.session_state.show_answer6 = False
    if 'show_explanation6' not in st.session_state:
        st.session_state.show_explanation6 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer6 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation6 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer6:
        st.markdown("""
        正確答案是 **？**""")

    if st.session_state.show_explanation6:
        st.markdown("""
        詳解：？。
        """)

# 題七
elif st.session_state.page == 8:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("推理思考 (1).png")
            st.image(image1, caption="練習題7")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("推理思考選項 (1).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["1", "2", "3", "4", "5"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer7' not in st.session_state:
        st.session_state.show_answer7 = False
    if 'show_explanation7' not in st.session_state:
        st.session_state.show_explanation7 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer7 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation7 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer7:
        st.markdown("""
        正確答案是 **4？**""")
        
    if st.session_state.show_explanation7:
        st.markdown("""
        詳解：？。
        """)

# 題八
elif st.session_state.page == 9:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("推理思考 (2).png")
            st.image(image1, caption="練習題8")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("推理思考選項 (2).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["1", "2", "3", "4", "5"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer8' not in st.session_state:
        st.session_state.show_answer8 = False
    if 'show_explanation8' not in st.session_state:
        st.session_state.show_explanation8 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer8 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation8 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer8:
        st.markdown("""
        正確答案是 **5**""")

    if st.session_state.show_explanation8:
        st.markdown("""
        詳解：外圓以大小間隔，內圓以逆時針轉動，線條以逆時針轉動並以在外圓裡外間隔。
        """)

# 題九
elif st.session_state.page == 10:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("羅桑二氏 (1).png")
            st.image(image1, caption="練習題9")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("羅桑二氏選項 (1).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["1", "2", "3", "4", "5"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer9' not in st.session_state:
        st.session_state.show_answer9 = False
    if 'show_explanation9' not in st.session_state:
        st.session_state.show_explanation9 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer9 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation9 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer9:
        st.markdown("""
        正確答案是 **4？**""")
        
    if st.session_state.show_explanation9:
        st.markdown("""
        詳解：？。
        """)

# 題十
elif st.session_state.page == 11:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

    # 顯示圖形題目與選項圖片
    col1, col2 = st.columns(2)
    with col1:
        try:
            image1 = Image.open("羅桑二氏 (2).png")
            st.image(image1, caption="練習題10")
        except FileNotFoundError:
            st.warning("⚠️ 圖片一載入失敗")
    
    with col2:
        try:
            image2 = Image.open("羅桑二氏選項 (2).png")
            st.image(image2, caption="請選擇您認為的正確圖形")
        except FileNotFoundError:
            st.warning("⚠️ 圖片二載入失敗")

    # 顯示選項（置中）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        answer = st.radio(
            label="選項",
            options=["1", "2", "3", "4", "5"],
            key="q_graphical_1",
            horizontal=True
        )

    # 初始化詳解狀態（只跑一次）
    if 'show_answer10' not in st.session_state:
        st.session_state.show_answer10 = False
    if 'show_explanation10' not in st.session_state:
        st.session_state.show_explanation10 = False

    # 三個按鈕：上一頁、看詳解、下一頁
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        st.button("上一頁", on_click=prev_page)

    with col3:
        if st.button("看答案"):
            st.session_state.show_answer10 = True

    with col4:
        if st.button("看詳解"):
            st.session_state.show_explanation10 = True

    with col6:
             st.button("下一頁", on_click=next_page)

    # ✅ 按下「看詳解」後才顯示詳解區塊
    if st.session_state.show_answer10:
        st.markdown("""
        正確答案是 **5**""")

    if st.session_state.show_explanation10:
        st.markdown("""
        詳解：外圓以大小間隔，內圓以逆時針轉動，線條以逆時針轉動並以在外圓裡外間隔。
        """)


# # 完成頁面
# elif st.session_state.page == 5:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
#     st.success("問卷已完成！非常感謝您的作答。")
#     st.balloons()
