import streamlit as st
import pandas as pd
import time
from PIL import Image

# 初始化分頁
if "page" not in st.session_state:
    st.session_state.page = 0

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
def prev_page():
    st.session_state.page -= 1
    st.session_state.scroll_to_top = True

def next_page():
    st.session_state.page += 1
    st.session_state.scroll_to_top = True
    
    if st.session_state.page == 1 and st.session_state.start_time is None:
        st.session_state.start_time = time.time()

# 顯示答案和詳解功能
def show_answer(page_number):
    st.session_state[f'show_answer_{page_number}'] = True

def show_explanation(page_number):
    st.session_state[f'show_explanation_{page_number}'] = True

# 初始化 session_state 的變數
if "page" not in st.session_state:
    st.session_state.page = 1

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "timer_started" not in st.session_state:
    st.session_state.timer_started = False

# 顯示計時器
if 2 < st.session_state.page < 13 and st.session_state.start_time:
    elapsed_seconds = int(time.time() - st.session_state.start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    st.markdown(f"⏱️ **練習時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 歡迎頁
if st.session_state.page == 0:
    st.header("歡迎參加本測驗")
    st.write("（此處將放上實驗說明與知情同意）")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col3:
        st.button("開始測驗", on_click=next_page)
            
# 基本資料頁
elif st.session_state.page == 1:
    if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
    st.header("基本資料")
    st.write("請填寫以下問卷，完成後按下一頁")
    age = st.radio("請問您是否為大專院校的學生？", ["是", "否"], index=None, key="age")
    gender = st.radio("請選擇您的性別", ["男", "女", "其他"], index=None, key="gender")
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])

    with col2:
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    with col4:
        if st.button("下一頁"):
            if age is None or gender is None:
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                st.session_state.warning_message = "" 
                st.session_state.page += 1
                st.rerun()

# 練習說明
elif st.session_state.page == 2:
    st.header("第一階段：練習測驗")
    st.write("此處將放上練習測驗說明")
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
    with col3:
        if st.button("開始練習"):
            st.session_state.start_time = time.time()
            st.session_state.timer_started = True
            st.session_state.page += 1  # 進入下一頁
            st.session_state.scroll_to_top = True
            st.rerun()
    
    with col4:
        if st.button("直接進入正式測驗"):
            st.session_state.page = 13
            st.session_state.scroll_to_top = True
            st.rerun()
    
# 高級圖形測驗函式
def graphical_question(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str,
    answer_value: str,
    explanation_text: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"練習題 {page_number-2}")
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
                label="",
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

        # 顯示答案與詳解
        if st.session_state[f'show_answer_{page_number}']:
            st.markdown(f"""正確答案是 **{answer_value}**""")

        if st.session_state[f'show_explanation_{page_number}']:
            st.markdown(f"""詳解：{explanation_text}""")

        # 三個按鈕
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col3:
            st.button("看答案", on_click=show_answer, args=(page_number,))
                
        with col4:
            st.button("看詳解", on_click=show_explanation, args=(page_number,))

        with col6:
            st.button("下一頁", on_click=next_page)

        col1, col2 = st.columns([7, 3])

        with col2:
            if st.button("直接進入正式測驗"):
                st.session_state.page = 13
                st.session_state.scroll_to_top = True
                st.rerun()
    
# 區分性向測驗函式
def graphical_question1(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str,
    answer_value: str,
    explanation_text: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"練習題 {page_number-2}")
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
                label="",
                options=["A", "B", "C", "D", "E"],
                key=radio_key,
                horizontal=True, 
                index=None
            )

        # 初始化詳解狀態（只跑一次）
        if f'show_answer_{page_number}' not in st.session_state:
            st.session_state[f'show_answer_{page_number}'] = False
        if f'show_explanation_{page_number}' not in st.session_state:
            st.session_state[f'show_explanation_{page_number}'] = False

        # 顯示答案與詳解
        if st.session_state[f'show_answer_{page_number}']:
            st.markdown(f"""正確答案是 **{answer_value}**""")

        if st.session_state[f'show_explanation_{page_number}']:
            st.markdown(f"""詳解：{explanation_text}""")

        # 三個按鈕
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col3:
            st.button("看答案", on_click=show_answer, args=(page_number,))
                
        with col4:
            st.button("看詳解", on_click=show_explanation, args=(page_number,))

        with col6:
            st.button("下一頁", on_click=next_page)
        
        col1, col2 = st.columns([7, 3])
        with col2:
            if st.button("直接進入正式測驗"):
                st.session_state.page = 13
                st.session_state.scroll_to_top = True
                st.rerun()

# 推理思考測驗&羅桑二氏非語文測驗函式
def graphical_question2(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str,
    answer_value: str,
    explanation_text: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"練習題 {page_number-2}")
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
                label="",
                options=["1", "2", "3", "4", "5"],
                key=radio_key,
                horizontal=True, 
                index=None
            )

        # 初始化詳解狀態（只跑一次）
        if f'show_answer_{page_number}' not in st.session_state:
            st.session_state[f'show_answer_{page_number}'] = False
        if f'show_explanation_{page_number}' not in st.session_state:
            st.session_state[f'show_explanation_{page_number}'] = False

        # 顯示答案與詳解
        if st.session_state[f'show_answer_{page_number}']:
            st.markdown(f"""正確答案是 **{answer_value}**""")

        if st.session_state[f'show_explanation_{page_number}']:
            st.markdown(f"""詳解：{explanation_text}""")

        # 三個按鈕
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col3:
            st.button("看答案", on_click=show_answer, args=(page_number,))
                
        with col4:
            st.button("看詳解", on_click=show_explanation, args=(page_number,))

        with col6:
            st.button("下一頁", on_click=next_page)
        
        col1, col2 = st.columns([7, 3])
        with col2:
            if st.button("直接進入正式測驗"):
                st.session_state.page = 13
                st.session_state.scroll_to_top = True
                st.rerun()

# 題一
graphical_question(
    page_number=3,
    question_image_path="高級圖形一 (1).png",
    option_image_path="高級圖形一選項 (1).png",
    radio_key="q_graphical_1",
    answer_value="8",
    explanation_text="本題中圖形的位置位於三條橫向點點線與一條直向直線處。"
)
      
# 題二
graphical_question(
    page_number=4,
    question_image_path="高級圖形一 (2).png",
    option_image_path="高級圖形一選項 (2).png",
    radio_key="q_graphical_2",
    answer_value="4",
    explanation_text="本題中圖形的位置位於一條橫向白線與一條直向白線，橫直白線的交會處皆會塗黑。"
)
        
# 題三
graphical_question(
    page_number=5,
    question_image_path="高級圖形二 (1).png",
    option_image_path="高級圖形二選項 (1).png",
    radio_key="q_graphical_3",
    answer_value="1",
    explanation_text="每一直排或每一橫排只會出現一次橫的與直的黑、白、斜線。"
)


# 題四
graphical_question(
    page_number=6,
    question_image_path="高級圖形二 (2).png",
    option_image_path="高級圖形二選項 (2).png",
    radio_key="q_graphical_4",
    answer_value="8",
    explanation_text="以橫向來看，第一張圖加上第二張圖會等於第三張，直向來看也是如此。"
)


# 題五
graphical_question1(
    page_number=7,
    question_image_path="區分 (1).png",
    option_image_path="區分選項 (1).png",
    radio_key="q_graphical_5",
    answer_value="E",
    explanation_text="箭頭以凹凸間隔，三角形以順時針轉動。"
)

# 題六
graphical_question1(
    page_number=8,
    question_image_path="區分 (2).png",
    option_image_path="區分選項 (2).png",
    radio_key="q_graphical_6",
    answer_value="2？",
    explanation_text="？。"
)
    
# 題七
graphical_question2(
    page_number=9,
    question_image_path="推理思考 (1).png",
    option_image_path="推理思考選項 (1).png",
    radio_key="q_graphical_7",
    answer_value="4？",
    explanation_text="？。"
)

# 題八
graphical_question2(
    page_number=10,
    question_image_path="推理思考 (2).png",
    option_image_path="推理思考選項 (2).png",
    radio_key="q_graphical_8",
    answer_value="5",
    explanation_text="外圓以大小間隔，內圓以逆時針轉動，線條以逆時針轉動並以在外圓裡外間隔。"
)

# 題九
graphical_question2(
    page_number=11,
    question_image_path="羅桑二氏 (1).png",
    option_image_path="羅桑二氏選項 (1).png",
    radio_key="q_graphical_9",
    answer_value="3",
    explanation_text="圖形皆是圓形，以大小間隔。"
)

# 題十
graphical_question2(
    page_number=12,
    question_image_path="羅桑二氏 (2).png",
    option_image_path="羅桑二氏選項 (2).png",
    radio_key="q_graphical_10",
    answer_value="4",
    explanation_text="圖形皆是由兩條線組成。"
)

#練習後問卷
if st.session_state.page == 13:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("進入正式測驗前")
    st.write("（此處將放個人知覺努力程度問題說明）")
    
    col1, col2= st.columns([3, 1])

    with col1:
        E1 = st.radio(label="您覺得自己有多認真對待剛才的練習題？",
                      options=["非常不認真", "不認真", "有點不認真", "有點認真", "認真", "非常認真"],
                      key="E1",
                      horizontal=True, 
                      index=None
                     )
        E2 = st.radio(label="您覺得自己有多投入於練習階段？",
                      options=["非常不投入", "不投入", "有點不投入", "有點投入", "投入", "非常投入"],
                      key="E2",
                      horizontal=True, 
                      index=None
                     )
        E3 = st.radio(label="您覺得自己在做練習題時有多努力？",
                      options=["非常不努力", "不努力", "有點不努力", "有點努力", "努力", "非常努力"],
                      key="E3",
                      horizontal=True, 
                      index=None
                     )
            
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    spacer1, btn_col = st.columns([5, 1])

    with btn_col:
        if st.button("下一頁"):
            if st.session_state.get("E1") is None or \
               st.session_state.get("E2") is None or \
               st.session_state.get("E3") is None:
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                st.session_state.warning_message = ""
                st.session_state.page += 1
                st.rerun()

# 正式測驗時間
if "formal_start_time" not in st.session_state:
    st.session_state.formal_start_time = None

if "formal_timer_started" not in st.session_state:
    st.session_state.formal_timer_started = False

# 顯示計時器
if 20 > st.session_state.page > 14 and st.session_state.formal_timer_started:
    elapsed_seconds = int(time.time() - st.session_state.formal_start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    st.markdown(f"⏱️ **正式測驗時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 正式測驗說明
if st.session_state.page == 14:
    st.header("第二階段：正式測驗")
    st.write("此處將放上正式測驗說明")
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
    with col3:
        if st.button("開始測驗"):
            st.session_state.formal_start_time = time.time()
            st.session_state.formal_timer_started = True
            st.session_state.page += 1  # 進入下一頁
            st.session_state.scroll_to_top = True
            st.rerun()

# 高級圖形測驗函式
def question(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"正式題 {page_number-14}")
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
                label="",
                options=["1", "2", "3", "4", "5", "6", "7", "8"],
                key=radio_key,
                horizontal=True, 
                index=None
            )

        # 三個按鈕
        warning_needed = False
        
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col6:
            if st.button("下一頁"):
                if st.session_state.get(radio_key) is None:
                    warning_needed = True  # 觸發提示
                else:
                    next_page()
                    st.rerun()
        
        if warning_needed:
            st.warning("⚠️ 請先作答才能繼續。")
    
# 區分性向測驗函式
def question1(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"正式題 {page_number-14}")
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
                label="",
                options=["A", "B", "C", "D", "E"],
                key=radio_key,
                horizontal=True, 
                index=None
            )

        # 三個按鈕
        warning_needed = False
        
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col6:
            if st.button("下一頁"):
                if st.session_state.get(radio_key) is None:
                    warning_needed = True  # 觸發提示
                else:
                    next_page()
                    st.rerun()
        
        if warning_needed:
            st.warning("⚠️ 請先作答才能繼續。")


# 推理思考測驗&羅桑二氏非語文測驗函式
def question2(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    radio_key: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"正式題 {page_number-14}")
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
                label="",
                options=["1", "2", "3", "4", "5"],
                key=radio_key,
                horizontal=True, 
                index=None
            )

        # 三個按鈕
        warning_needed = False
        
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col6:
            if st.button("下一頁"):
                if st.session_state.get(radio_key) is None:
                    warning_needed = True  # 觸發提示
                else:
                    next_page()
                    st.rerun()
        
        if warning_needed:
            st.warning("⚠️ 請先作答才能繼續。")


# 1
question(
    page_number=15,
    question_image_path="高級圖形一 (5).png",
    option_image_path="高級圖形一選項 (5).png",
    radio_key="q_1"
)
        
# 2
question(
    page_number=16,
    question_image_path="高級圖形二 (5).png",
    option_image_path="高級圖形二選項 (5).png",
    radio_key="q_2"
)

# 3
question1(
    page_number=17,
    question_image_path="區分 (5).png",
    option_image_path="區分選項 (5).png",
    radio_key="q_3",
)

# 4
question2(
    page_number=18,
    question_image_path="推理思考 (5).png",
    option_image_path="推理思考選項 (5).png",
    radio_key="q_4"
)

# 5
question2(
    page_number=19,
    question_image_path="羅桑二氏 (5).png",
    option_image_path="羅桑二氏選項 (5).png",
    radio_key="q_5",
)

if st.session_state.page == 20:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
                /* 強制整頁白底，清除殘影 */
                body, .main, .block-container {
                    background-color: white !important;
                }

                /* 置頂區塊容器 */
                .top-container {
                    padding-top: 30px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                /* 將進度條的外框撐寬（選擇性） */
                .stProgress {
                    width: 60%;
                    margin: 0 auto;
                }
            </style>
            <div class="top-container">
                <h4>⏳ 資料處理中，請稍候…</h4>
            </div>
        """, unsafe_allow_html=True)

        # 放置進度條（放在 Markdown 之後，就會靠近頂部）
        progress_bar = st.progress(0)

    for i in range(10):
        time.sleep(0.5)
        progress_bar.progress((i + 1) * 10)

    # 處理完跳轉下一頁
    st.session_state.page += 1
    st.session_state.scroll_to_top = True
    st.rerun()
    
if st.session_state.page == 21:
    st.header("📋 測驗結果")

    if st.session_state.get("formal_start_time"):
        elapsed_seconds = int(time.time() - st.session_state.formal_start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_str = f"{minutes} 分 {seconds} 秒"
    else:
        time_str = "無法取得"

    # 模擬分數
    personal_score = 65
    average_score = 80

    # 使用 Pandas 資料表呈現
    import pandas as pd
    result_df = pd.DataFrame({
        "項目": ["您的測驗分數", "同齡他人平均分數", "您花費的時間"],
        "結果": [f"{personal_score} / 100", f"{average_score} / 100", time_str]
    })

    st.table(result_df)

    # 下一頁按鈕
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("下一頁"):
            st.session_state.page += 1
            st.session_state.scroll_to_top = True
            st.rerun()
   

# 測驗後問卷
if st.session_state.page == 22:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("結束正式測驗前")
    st.write("（此處將放依變項問題說明）")
    
    col1, col2= st.columns([3, 1])
    
    with col1:
        E1 = st.radio(label="您認為自己的邏輯推理能力如何？",
                      options=["非常不好", "不好", "有點不好", "有點好", "好", "非常好"],
                      key="E1",
                      horizontal=True, 
                      index=None
                     )
        E2 = st.radio(label="您認為自己的分析思考能力如何？",
                      options=["非常不好", "不好", "有點不好", "有點好", "好", "非常好"],
                      key="E2",
                      horizontal=True, 
                      index=None
                     )
        E3 = st.radio(label="您認為自己的圖形理解能力如何？",
                      options=["非常不好", "不好", "有點不好", "有點好", "好", "非常好"],
                      key="E3",
                      horizontal=True, 
                      index=None
                     )
            
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    spacer1, btn_col = st.columns([5, 1])

    with btn_col:
        if st.button("下一頁"):
            if st.session_state.get("E1") is None or \
               st.session_state.get("E2") is None or \
               st.session_state.get("E3") is None:
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                st.session_state.warning_message = ""
                st.session_state.page += 1
                st.rerun()


# # 完成頁面
# elif st.session_state.page == 5:
#     st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
#     st.success("問卷已完成！非常感謝您的作答。")
#     st.balloons()
