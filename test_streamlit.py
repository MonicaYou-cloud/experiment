import streamlit as st
import pandas as pd
import time
from PIL import Image
import streamlit.components.v1 as components

# 放在每一頁的最上面來捲動到頂部
def scroll_top():
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)

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
if 'go_next' not in st.session_state:
    st.session_state.go_next = False
if 'go_prev' not in st.session_state:
    st.session_state.go_prev = False

# 換頁函式：設定旗標
def next_page():
    st.session_state.go_next = True
def prev_page():
    st.session_state.go_prev = True

# ⏱️ 換頁觸發後，實際處理與初始化計時
if st.session_state.go_next:
    st.session_state.page += 1
    st.session_state.go_next = False
    if st.session_state.page == 1 and st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    st.rerun()

if st.session_state.go_prev:
    st.session_state.page -= 1
    st.session_state.go_prev = False
    st.rerun()

# 顯示計時器
if st.session_state.page > 0 and st.session_state.start_time:
    elapsed_seconds = int(time.time() - st.session_state.start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    st.markdown(f"⏱️ **測驗時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 歡迎頁
if st.session_state.page == 0:
    st.title("歡迎參加本測驗")
    st.write("本測驗包含數題圖片與選項，請專心作答。")
    st.button("開始測驗", on_click=next_page)


# 基本資料頁
elif st.session_state.page == 1:
    st.header("基本資料")
    st.write("請填寫以下問卷，完成後按下一頁。")

    # 問題選項，加上 key 儲存在 session_state
    st.radio("請問您是否為大專院校的學生？", ["是", "否"], index=None, key="age")
    st.radio("請選擇您的性別", ["男", "女", "其他"], index=None, key="gender")

    if st.button("下一頁"):
        if st.session_state.age is None or st.session_state.gender is None:
            st.warning("請完整填寫所有問題才能繼續。")
        else:
            st.session_state.page += 1
            st.rerun()  # ✅ 避免需要按兩下的問題
            
#高級圖形測驗函式
def graphical_question(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str,
    answer_value: str,
    explanation_text: str
):
    if st.session_state.page == page_number:
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"練習題 {page_number-1}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片一載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇您認為的正確圖形")
            except FileNotFoundError:
                st.warning("⚠️ 圖片二載入失敗")

        # 顯示選項（置中）
        col1, col2, col3 = st.columns([1, 5, 1])
        with col2:
            answer = st.radio(
                label="選項",
                options=["1", "2", "3", "4", "5", "6", "7", "8"],
                key=radio_key,
                horizontal=True, 
                index=None
            )

        # 初始化詳解狀態（只跑一次）
        if f'show_answer_{page_number}' not in st.session_state:
            st.session_state[f'show_answer_{page_number}'] = False
        if f'show_explanation_{page_number}' not in st.session_state:
            st.session_state[f'show_explanation_{page_number}'] = False

        # 三個按鈕
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col3:
            if st.button("看答案"):
                st.session_state[f'show_answer_{page_number}'] = True

        with col4:
            if st.button("看詳解"):
                st.session_state[f'show_explanation_{page_number}'] = True

        with col6:
            st.button("下一頁", on_click=next_page)

        # 顯示答案與詳解
        if st.session_state[f'show_answer_{page_number}']:
            st.markdown(f"""正確答案是 **{answer_value}**""")

        if st.session_state[f'show_explanation_{page_number}']:
            st.markdown(f"""詳解：{explanation_text}""")

#區分性向測驗函式
def graphical_question1(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str,
    answer_value: str,
    explanation_text: str
):
    if st.session_state.page == page_number:
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"練習題 {page_number-1}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片一載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇您認為的正確圖形")
            except FileNotFoundError:
                st.warning("⚠️ 圖片二載入失敗")

        # 顯示選項（置中）
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            answer = st.radio(
                label="選項",
                options=["A", "B", "C", "D", "E"],
                key="q_graphical_5",
                horizontal=True, 
                index=None
            )

        # 初始化詳解狀態（只跑一次）
        if f'show_answer_{page_number}' not in st.session_state:
            st.session_state[f'show_answer_{page_number}'] = False
        if f'show_explanation_{page_number}' not in st.session_state:
            st.session_state[f'show_explanation_{page_number}'] = False

        # 三個按鈕
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col3:
            if st.button("看答案"):
                st.session_state[f'show_answer_{page_number}'] = True

        with col4:
            if st.button("看詳解"):
                st.session_state[f'show_explanation_{page_number}'] = True

        with col6:
            st.button("下一頁", on_click=next_page)

        # 顯示答案與詳解
        if st.session_state[f'show_answer_{page_number}']:
            st.markdown(f"""✅ 正確答案是 **{answer_value}**""")

        if st.session_state[f'show_explanation_{page_number}']:
            st.markdown(f"""📘 詳解：{explanation_text}""")

# 題一
graphical_question(
    page_number=2,
    question_image_path="高級圖形一 (1).png",
    option_image_path="高級圖形一選項 (1).png",
    radio_key="q_graphical_1",
    answer_value="8",
    explanation_text="本題中圖形的位置位於三條橫向點點線與一條直向直線處。"
)
      
# 題二
graphical_question(
    page_number=3,
    question_image_path="高級圖形一 (2).png",
    option_image_path="高級圖形一選項 (2).png",
    radio_key="q_graphical_2",
    answer_value="4",
    explanation_text="本題中圖形的位置位於一條橫向白線與一條直向白線，橫直白線的交會處皆會塗黑。"
)
        
# 題三
graphical_question(
    page_number=4,
    question_image_path="高級圖形二 (1).png",
    option_image_path="高級圖形二選項 (1).png",
    radio_key="q_graphical_3",
    answer_value="1",
    explanation_text="每一直排或每一橫排只會出現一次橫的與直的黑、白、斜線。"
)


# 題四
graphical_question(
    page_number=5,
    question_image_path="高級圖形二 (2).png",
    option_image_path="高級圖形二選項 (2).png",
    radio_key="q_graphical_4",
    answer_value="8",
    explanation_text="以橫向來看，第一張圖加上第二張圖會等於第三張，直向來看也是如此。"
)


# 題五
graphical_question1(
    page_number=6,
    question_image_path="區分 (1).png",
    option_image_path="區分選項 (1).png",
    radio_key="q_graphical_5",
    answer_value="E",
    explanation_text="箭頭以凹凸間隔，三角形以順時針轉動。"
)

# 題六
graphical_question1(
    page_number=7,
    question_image_path="區分 (2).png",
    option_image_path="區分選項 (2).png",
    radio_key="q_graphical_6",
    answer_value="？",
    explanation_text="？。"
)
    




# # 題七
# elif st.session_state.page == 8:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

#     # 顯示圖形題目與選項圖片
#     col1, col2 = st.columns(2)
#     with col1:
#         try:
#             image1 = Image.open("推理思考 (1).png")
#             st.image(image1, caption="練習題7")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片一載入失敗")
    
#     with col2:
#         try:
#             image2 = Image.open("推理思考選項 (1).png")
#             st.image(image2, caption="請選擇您認為的正確圖形")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片二載入失敗")

#     # 顯示選項（置中）
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         answer = st.radio(
#             label="選項",
#             options=["1", "2", "3", "4", "5"],
#             key="q_graphical_7",
#             horizontal=True, 
#             index=None
#         )

#     # 初始化詳解狀態（只跑一次）
#     if 'show_answer7' not in st.session_state:
#         st.session_state.show_answer7 = False
#     if 'show_explanation7' not in st.session_state:
#         st.session_state.show_explanation7 = False

#     # 三個按鈕：上一頁、看詳解、下一頁
#     col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

#     with col1:
#         st.button("上一頁", on_click=prev_page)

#     with col3:
#         if st.button("看答案"):
#             st.session_state.show_answer7 = True

#     with col4:
#         if st.button("看詳解"):
#             st.session_state.show_explanation7 = True

#     with col6:
#              st.button("下一頁", on_click=next_page)

#     # ✅ 按下「看詳解」後才顯示詳解區塊
#     if st.session_state.show_answer7:
#         st.markdown("""
#         正確答案是 **4？**""")
        
#     if st.session_state.show_explanation7:
#         st.markdown("""
#         詳解：？。
#         """)

# # 題八
# elif st.session_state.page == 9:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

#     # 顯示圖形題目與選項圖片
#     col1, col2 = st.columns(2)
#     with col1:
#         try:
#             image1 = Image.open("推理思考 (2).png")
#             st.image(image1, caption="練習題8")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片一載入失敗")
    
#     with col2:
#         try:
#             image2 = Image.open("推理思考選項 (2).png")
#             st.image(image2, caption="請選擇您認為的正確圖形")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片二載入失敗")

#     # 顯示選項（置中）
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         answer = st.radio(
#             label="選項",
#             options=["1", "2", "3", "4", "5"],
#             key="q_graphical_8",
#             horizontal=True, 
#             index=None
#         )

#     # 初始化詳解狀態（只跑一次）
#     if 'show_answer8' not in st.session_state:
#         st.session_state.show_answer8 = False
#     if 'show_explanation8' not in st.session_state:
#         st.session_state.show_explanation8 = False

#     # 三個按鈕：上一頁、看詳解、下一頁
#     col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

#     with col1:
#         st.button("上一頁", on_click=prev_page)

#     with col3:
#         if st.button("看答案"):
#             st.session_state.show_answer8 = True

#     with col4:
#         if st.button("看詳解"):
#             st.session_state.show_explanation8 = True

#     with col6:
#              st.button("下一頁", on_click=next_page)

#     # ✅ 按下「看詳解」後才顯示詳解區塊
#     if st.session_state.show_answer8:
#         st.markdown("""
#         正確答案是 **5**""")

#     if st.session_state.show_explanation8:
#         st.markdown("""
#         詳解：外圓以大小間隔，內圓以逆時針轉動，線條以逆時針轉動並以在外圓裡外間隔。
#         """)

# # 題九
# elif st.session_state.page == 10:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

#     # 顯示圖形題目與選項圖片
#     col1, col2 = st.columns(2)
#     with col1:
#         try:
#             image1 = Image.open("羅桑二氏 (1).png")
#             st.image(image1, caption="練習題9")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片一載入失敗")
    
#     with col2:
#         try:
#             image2 = Image.open("羅桑二氏選項 (1).png")
#             st.image(image2, caption="請選擇您認為的正確圖形")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片二載入失敗")

#     # 顯示選項（置中）
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         answer = st.radio(
#             label="選項",
#             options=["1", "2", "3", "4", "5"],
#             key="q_graphical_9",
#             horizontal=True, 
#             index=None
#         )

#     # 初始化詳解狀態（只跑一次）
#     if 'show_answer9' not in st.session_state:
#         st.session_state.show_answer9 = False
#     if 'show_explanation9' not in st.session_state:
#         st.session_state.show_explanation9 = False

#     # 三個按鈕：上一頁、看詳解、下一頁
#     col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

#     with col1:
#         st.button("上一頁", on_click=prev_page)

#     with col3:
#         if st.button("看答案"):
#             st.session_state.show_answer9 = True

#     with col4:
#         if st.button("看詳解"):
#             st.session_state.show_explanation9 = True

#     with col6:
#              st.button("下一頁", on_click=next_page)

#     # ✅ 按下「看詳解」後才顯示詳解區塊
#     if st.session_state.show_answer9:
#         st.markdown("""
#         正確答案是 **3**""")
        
#     if st.session_state.show_explanation9:
#         st.markdown("""
#         詳解：圖形皆是圓形，以大小間隔。
#         """)

# # 題十
# elif st.session_state.page == 11:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)

#     # 顯示圖形題目與選項圖片
#     col1, col2 = st.columns(2)
#     with col1:
#         try:
#             image1 = Image.open("羅桑二氏 (2).png")
#             st.image(image1, caption="練習題10")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片一載入失敗")
    
#     with col2:
#         try:
#             image2 = Image.open("羅桑二氏選項 (2).png")
#             st.image(image2, caption="請選擇您認為的正確圖形")
#         except FileNotFoundError:
#             st.warning("⚠️ 圖片二載入失敗")

#     # 顯示選項（置中）
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         answer = st.radio(
#             label="選項",
#             options=["1", "2", "3", "4", "5"],
#             key="q_graphical_10",
#             horizontal=True, 
#             index=None
#         )

#     # 初始化詳解狀態（只跑一次）
#     if 'show_answer10' not in st.session_state:
#         st.session_state.show_answer10 = False
#     if 'show_explanation10' not in st.session_state:
#         st.session_state.show_explanation10 = False

#     # 三個按鈕：上一頁、看詳解、下一頁
#     col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

#     with col1:
#         st.button("上一頁", on_click=prev_page)

#     with col3:
#         if st.button("看答案"):
#             st.session_state.show_answer10 = True

#     with col4:
#         if st.button("看詳解"):
#             st.session_state.show_explanation10 = True

#     with col6:
#              st.button("下一頁", on_click=next_page)

#     # ✅ 按下「看詳解」後才顯示詳解區塊
#     if st.session_state.show_answer10:
#         st.markdown("""
#         正確答案是 **4**""")

#     if st.session_state.show_explanation10:
#         st.markdown("""
#         詳解：圖形皆是由兩條線組成。
#         """)

# scroll_top()


# # 完成頁面
# elif st.session_state.page == 5:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
#     st.success("問卷已完成！非常感謝您的作答。")
#     st.balloons()
