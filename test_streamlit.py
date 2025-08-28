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

# 顯示答案功能
def show_answer(page_number):
    st.session_state[f'show_answer_{page_number}'] = True

# 初始化 session_state 的變數
if "page" not in st.session_state:
    st.session_state.page = 1

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "timer_started" not in st.session_state:
    st.session_state.timer_started = False

# 顯示計時器
if 2 < st.session_state.page < 103 and st.session_state.start_time:
    elapsed_seconds = int(time.time() - st.session_state.start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    st.markdown(f"⏱️ **練習時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 歡迎頁
if st.session_state.page == 0:
    st.header("歡迎參加本測驗")
    st.markdown("---")
    st.write("（此處將放上實驗說明與知情同意）")
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col3:
        st.button("開始測驗", on_click=next_page)
            
# 基本資料頁
elif st.session_state.page == 1:
    if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
    st.header("基本資料")
    st.markdown("---")
    st.write("請填寫以下問卷，完成後按下一頁")
    age = st.radio("請問您是否為大專院校的學生？", ["是", "否"], index=None, key="age")
    gender = st.radio("請選擇您的生理性別", ["男", "女", "其他"], index=None, key="gender")
    self_esteem1 = st.radio("我覺得自己一無是處。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem1")
    self_esteem2 = st.radio("我有許多優點。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem2")
    self_esteem3 = st.radio("我能像大多數人一樣做好事情。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem3")
    self_esteem4 = st.radio("我沒有什麼值得驕傲的地方。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem4")
    self_esteem5 = st.radio("我很沒用。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem5")
    self_esteem6 = st.radio("我是一個有價值的人。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem6")
    self_esteem7 = st.radio("我希望我能更尊重自己。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem7")
    self_esteem8 = st.radio("整體來說，我是個失敗者。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem8")
    self_esteem9 = st.radio("我對自己抱持正面的態度。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem9")
    self_esteem10 = st.radio("整體來說，我對自己感到滿意。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="self_esteem10")
    mindset1 = st.radio("人的聰明程度是固定的，無論做什麼都不能改變。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="mindset1")
    mindset2 = st.radio("人可以學新的東西，但沒有辦法真正改變自己原本的聰明程度。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="mindset2")
    mindset3 = st.radio("一個人有多聰明是他不太能夠改變的。", ["非常不同意", "不同意", "有點不同意", "有點同意", "同意", "非常同意"], index=None, key="mindset3")
    important1 = st.radio("對您來說，邏輯推理能力是否重要？", ["非常不重要", "不重要", "有點不重要", "有點重要", "重要", "非常重要"], index=None, key="important1")
    important2 = st.radio("對您來說，分析思考能力是否重要？", ["非常不重要", "不重要", "有點不重要", "有點重要", "重要", "非常重要"], index=None, key="important2")
    important3 = st.radio("對您來說，圖形理解能力是否重要？", ["非常不重要", "不重要", "有點不重要", "有點重要", "重要", "非常重要"], index=None, key="important3")
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col2:
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    with col4:
        if st.button("下一頁"):
            if (age is None or gender is None or self_esteem1 is None or self_esteem2 is None or self_esteem3 is None 
                or self_esteem4 is None or self_esteem5 is None or self_esteem6 is None or self_esteem7 is None 
                or self_esteem8 is None or self_esteem9 is None or self_esteem10 is None or mindset1 is None 
                or mindset2 is None or mindset3 is None or important1 is None or important2 is None or important3 is None):
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                st.session_state.warning_message = "" 
                st.session_state.page += 1
                st.rerun()

# 練習說明
elif st.session_state.page == 2:
    st.header("第一階段：練習測驗")
    st.markdown("---")
    st.write("此處將放上練習測驗說明")
    st.markdown("---")
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
            st.session_state.start_time = None
            st.session_state.page = 105
            st.session_state.scroll_to_top = True
            st.rerun()
    
# 練習測驗函式
def graphical_question(
    page_number: int,
    question_image_path: str,
    option_image_path: str,
    answer_value: str
):
    if st.session_state.page == page_number:
        if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
        
        if f'show_answer_{page_number}' not in st.session_state:
            st.session_state[f'show_answer_{page_number}'] = False
        # 顯示圖形題目與選項圖片
        col1, col2 = st.columns(2)
        with col1:
            try:
                image1 = Image.open(question_image_path)
                st.image(image1, caption=f"練習題 {page_number-2}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇您認為的正確圖形")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")

        # 顯示答案
        if st.session_state[f'show_answer_{page_number}']:
            st.markdown(f"""正確答案是 **{answer_value}**""")

        # 三個按鈕
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

        with col1:
            st.button("上一頁", on_click=prev_page)

        with col3:
            st.button("看答案", on_click=show_answer, args=(page_number,))

        with col5:
            st.button("下一頁", on_click=next_page)

        col1, col2 = st.columns([7, 3])

        with col2:
            if st.button("直接進入正式測驗"):
                st.session_state.page = 105
                st.session_state.scroll_to_top = True
                st.rerun()
    
# 練題1
graphical_question(
    page_number=3,
    question_image_path="new_folder/高級圖形一 (3).png",
    option_image_path="new_folder/高級圖形一選項 (3).png",
    answer_value=""
)
      
# 練題2
graphical_question(
    page_number=4,
    question_image_path="new_folder/高級圖形二 (19).png",
    option_image_path="new_folder/高級圖形二選項 (19).png",
    answer_value=""
)
        
# 練題3
graphical_question(
    page_number=5,
    question_image_path="new_folder/高級圖形二 (18).png",
    option_image_path="new_folder/高級圖形二選項 (18).png",
    answer_value=""
)


# 練題4
graphical_question(
    page_number=6,
    question_image_path="new_folder/高級圖形二 (23).png",
    option_image_path="new_folder/高級圖形二選項 (23).png",
    answer_value=""
)


# 練題5
graphical_question(
    page_number=7,
    question_image_path="new_folder/區分 (24).png",
    option_image_path="new_folder/區分選項 (24).png",
    answer_value=""
)

# 練題6
graphical_question(
    page_number=8,
    question_image_path="new_folder/區分 (4).png",
    option_image_path="new_folder/區分選項 (4).png",
    answer_value=""
)
    
# 練題7
graphical_question(
    page_number=9,
    question_image_path="new_folder/區分 (18).png",
    option_image_path="new_folder/區分選項 (18).png",
    answer_value=""
)

# 練題8
graphical_question(
    page_number=10,
    question_image_path="new_folder/推理思考 (8).png",
    option_image_path="new_folder/推理思考選項 (8).png",
    answer_value=""
)

# 練題9
graphical_question(
    page_number=11,
    question_image_path="new_folder/羅桑二氏 (51).png",
    option_image_path="new_folder/羅桑二氏選項 (51).png",
    answer_value=""
)

# 練題10
graphical_question(
    page_number=12,
    question_image_path="new_folder/羅桑二氏 (16).png",
    option_image_path="new_folder/羅桑二氏選項 (16).png",
    answer_value=""
)

# 練題11
graphical_question(
    page_number=13,
    question_image_path="new_folder/高級圖形一 (8).png",
    option_image_path="new_folder/高級圖形一選項 (8).png",
    answer_value=""
)
      
# 練題12
graphical_question(
    page_number=14,
    question_image_path="new_folder/高級圖形二 (28).png",
    option_image_path="new_folder/高級圖形二選項 (28).png",
    answer_value=""
)
        
# 練題13
graphical_question(
    page_number=15,
    question_image_path="new_folder/高級圖形二 (32).png",
    option_image_path="new_folder/高級圖形二選項 (32).png",
    answer_value=""
)


# 練題14
graphical_question(
    page_number=16,
    question_image_path="new_folder/區分 (17).png",
    option_image_path="new_folder/區分選項 (17).png",
    answer_value=""
)


# 練題15
graphical_question(
    page_number=17,
    question_image_path="new_folder/區分 (14).png",
    option_image_path="new_folder/區分選項 (14).png",
    answer_value=""
)

# 練題16
graphical_question(
    page_number=18,
    question_image_path="new_folder/區分 (12).png",
    option_image_path="new_folder/區分選項 (12).png",
    answer_value=""
)
    
# 練題17
graphical_question(
    page_number=19,
    question_image_path="new_folder/推理思考 (6).png",
    option_image_path="new_folder/推理思考選項 (6).png",
    answer_value=""
)

# 練題18
graphical_question(
    page_number=20,
    question_image_path="new_folder/推理思考 (11).png",
    option_image_path="new_folder/推理思考選項 (11).png",
    answer_value=""
)

# 練題19
graphical_question(
    page_number=21,
    question_image_path="new_folder/羅桑二氏 (3).png",
    option_image_path="new_folder/羅桑二氏選項 (3).png",
    answer_value=""
)

# 練題20
graphical_question(
    page_number=22,
    question_image_path="new_folder/羅桑二氏 (47).png",
    option_image_path="new_folder/羅桑二氏選項 (47).png",
    answer_value=""
)

# 練題21
graphical_question(
    page_number=23,
    question_image_path="new_folder/高級圖形一 (2).png",
    option_image_path="new_folder/高級圖形一選項 (2).png",
    answer_value=""
)
      
# 練題22
graphical_question(
    page_number=24,
    question_image_path="new_folder/高級圖形二 (21).png",
    option_image_path="new_folder/高級圖形二選項 (21).png",
    answer_value=""
)
        
# 練題23
graphical_question(
    page_number=25,
    question_image_path="new_folder/高級圖形二 (4).png",
    option_image_path="new_folder/高級圖形二選項 (4).png",
    answer_value=""
)


# 練題24
graphical_question(
    page_number=26,
    question_image_path="new_folder/區分 (23).png",
    option_image_path="new_folder/區分選項 (23).png",
    answer_value=""
)


# 練題25
graphical_question(
    page_number=27,
    question_image_path="new_folder/區分 (32).png",
    option_image_path="new_folder/區分選項 (32).png",
    answer_value=""
)

# 練題26
graphical_question(
    page_number=28,
    question_image_path="new_folder/區分 (11).png",
    option_image_path="new_folder/區分選項 (11).png",
    answer_value=""
)
    
# 練題27
graphical_question(
    page_number=29,
    question_image_path="new_folder/推理思考 (12).png",
    option_image_path="new_folder/推理思考選項 (12).png",
    answer_value=""
)

# 練題28
graphical_question(
    page_number=30,
    question_image_path="new_folder/推理思考 (13).png",
    option_image_path="new_folder/推理思考選項 (13).png",
    answer_value=""
)

# 練題29
graphical_question(
    page_number=31,
    question_image_path="new_folder/羅桑二氏 (33).png",
    option_image_path="new_folder/羅桑二氏選項 (33).png",
    answer_value=""
)

# 練題30
graphical_question(
    page_number=32,
    question_image_path="new_folder/羅桑二氏 (54).png",
    option_image_path="new_folder/羅桑二氏選項 (54).png",
    answer_value=""
)

# 練題31
graphical_question(
    page_number=33,
    question_image_path="new_folder/高級圖形一 (6).png",
    option_image_path="new_folder/高級圖形一選項 (6).png",
    answer_value=""
)
      
# 練題32
graphical_question(
    page_number=34,
    question_image_path="new_folder/高級圖形二 (26).png",
    option_image_path="new_folder/高級圖形二選項 (26).png",
    answer_value=""
)
        
# 練題33
graphical_question(
    page_number=35,
    question_image_path="new_folder/高級圖形二 (13).png",
    option_image_path="new_folder/高級圖形二選項 (13).png",
    answer_value=""
)


# 練題34
graphical_question(
    page_number=36,
    question_image_path="new_folder/高級圖形二 (9).png",
    option_image_path="new_folder/高級圖形二選項 (9).png",
    answer_value=""
)


# 練題35
graphical_question(
    page_number=37,
    question_image_path="new_folder/區分 (16).png",
    option_image_path="new_folder/區分選項 (16).png",
    answer_value=""
)

# 練題36
graphical_question(
    page_number=38,
    question_image_path="new_folder/區分 (31).png",
    option_image_path="new_folder/區分選項 (31).png",
    answer_value=""
)
    
# 練題37
graphical_question(
    page_number=39,
    question_image_path="new_folder/區分 (26).png",
    option_image_path="new_folder/區分選項 (26).png",
    answer_value=""
)

# 練題38
graphical_question(
    page_number=40,
    question_image_path="new_folder/推理思考 (14).png",
    option_image_path="new_folder/推理思考選項 (14).png",
    answer_value=""
)

# 練題39
graphical_question(
    page_number=41,
    question_image_path="new_folder/羅桑二氏 (59).png",
    option_image_path="new_folder/羅桑二氏選項 (59).png",
    answer_value=""
)

# 練題40
graphical_question(
    page_number=42,
    question_image_path="new_folder/羅桑二氏 (57).png",
    option_image_path="new_folder/羅桑二氏選項 (57).png",
    answer_value=""
)

# 練題41
graphical_question(
    page_number=43,
    question_image_path="new_folder/高級圖形一 (9).png",
    option_image_path="new_folder/高級圖形一選項 (9).png",
    answer_value=""
)
      
# 練題42
graphical_question(
    page_number=44,
    question_image_path="new_folder/高級圖形二 (29).png",
    option_image_path="new_folder/高級圖形二選項 (29).png",
    answer_value=""
)
        
# 練題43
graphical_question(
    page_number=45,
    question_image_path="new_folder/高級圖形二 (34).png",
    option_image_path="new_folder/高級圖形二選項 (34).png",
    answer_value=""
)


# 練題44
graphical_question(
    page_number=46,
    question_image_path="new_folder/高級圖形二 (17).png",
    option_image_path="new_folder/高級圖形二選項 (17).png",
    answer_value=""
)


# 練題45
graphical_question(
    page_number=47,
    question_image_path="new_folder/區分 (34).png",
    option_image_path="new_folder/區分選項 (34).png",
    answer_value=""
)

# 練題46
graphical_question(
    page_number=48,
    question_image_path="new_folder/區分 (1).png",
    option_image_path="new_folder/區分選項 (1).png",
    answer_value=""
)
    
# 練題47
graphical_question(
    page_number=49,
    question_image_path="new_folder/區分 (9).png",
    option_image_path="new_folder/區分選項 (9).png",
    answer_value=""
)

# 練題48
graphical_question(
    page_number=50,
    question_image_path="new_folder/推理思考 (16).png",
    option_image_path="new_folder/推理思考選項 (16).png",
    answer_value=""
)

# 練題49
graphical_question(
    page_number=51,
    question_image_path="new_folder/羅桑二氏 (36).png",
    option_image_path="new_folder/羅桑二氏選項 (36).png",
    answer_value=""
)

# 練題50
graphical_question(
    page_number=52,
    question_image_path="new_folder/羅桑二氏 (18).png",
    option_image_path="new_folder/羅桑二氏選項 (18).png",
    answer_value=""
)

# 練題51
graphical_question(
    page_number=53,
    question_image_path="new_folder/高級圖形一 (1).png",
    option_image_path="new_folder/高級圖形一選項 (1).png",
    answer_value=""
)
      
# 練題52
graphical_question(
    page_number=54,
    question_image_path="new_folder/高級圖形二 (8).png",
    option_image_path="new_folder/高級圖形二選項 (8).png",
    answer_value=""
)
        
# 練題53
graphical_question(
    page_number=55,
    question_image_path="new_folder/高級圖形二 (33).png",
    option_image_path="new_folder/高級圖形二選項 (33).png",
    answer_value=""
)


# 練題54
graphical_question(
    page_number=56,
    question_image_path="new_folder/區分 (3).png",
    option_image_path="new_folder/區分選項 (3).png",
    answer_value=""
)


# 練題55
graphical_question(
    page_number=57,
    question_image_path="new_folder/區分 (36).png",
    option_image_path="new_folder/區分選項 (36).png",
    answer_value=""
)

# 練題56
graphical_question(
    page_number=58,
    question_image_path="new_folder/區分 (22).png",
    option_image_path="new_folder/區分選項 (22).png",
    answer_value=""
)
    
# 練題57
graphical_question(
    page_number=59,
    question_image_path="new_folder/推理思考 (18).png",
    option_image_path="new_folder/推理思考選項 (18).png",
    answer_value=""
)

# 練題58
graphical_question(
    page_number=60,
    question_image_path="new_folder/推理思考 (3).png",
    option_image_path="new_folder/推理思考選項 (3).png",
    answer_value=""
)

# 練題59
graphical_question(
    page_number=61,
    question_image_path="new_folder/羅桑二氏 (19).png",
    option_image_path="new_folder/羅桑二氏選項 (19).png",
    answer_value=""
)

# 練題60
graphical_question(
    page_number=62,
    question_image_path="new_folder/羅桑二氏 (45).png",
    option_image_path="new_folder/羅桑二氏選項 (45).png",
    answer_value=""
)

# 練題61
graphical_question(
    page_number=63,
    question_image_path="new_folder/高級圖形一 (12).png",
    option_image_path="new_folder/高級圖形一選項 (12).png",
    answer_value=""
)
      
# 練題62
graphical_question(
    page_number=64,
    question_image_path="new_folder/高級圖形二 (14).png",
    option_image_path="new_folder/高級圖形二選項 (14).png",
    answer_value=""
)
        
# 練題63
graphical_question(
    page_number=65,
    question_image_path="new_folder/高級圖形二 (27).png",
    option_image_path="new_folder/高級圖形二選項 (27).png",
    answer_value=""
)


# 練題64
graphical_question(
    page_number=66,
    question_image_path="new_folder/區分 (33).png",
    option_image_path="new_folder/區分選項 (33).png",
    answer_value=""
)


# 練題65
graphical_question(
    page_number=67,
    question_image_path="new_folder/區分 (2).png",
    option_image_path="new_folder/區分選項 (2).png",
    answer_value=""
)

# 練題66
graphical_question(
    page_number=68,
    question_image_path="new_folder/區分 (6).png",
    option_image_path="new_folder/區分選項 (6).png",
    answer_value=""
)
    
# 練題67
graphical_question(
    page_number=69,
    question_image_path="new_folder/推理思考 (19).png",
    option_image_path="new_folder/推理思考選項 (19).png",
    answer_value=""
)

# 練題68
graphical_question(
    page_number=70,
    question_image_path="new_folder/推理思考 (4).png",
    option_image_path="new_folder/推理思考選項 (4).png",
    answer_value=""
)

# 練題69
graphical_question(
    page_number=71,
    question_image_path="new_folder/羅桑二氏 (44).png",
    option_image_path="new_folder/羅桑二氏選項 (44).png",
    answer_value=""
)

# 練題70
graphical_question(
    page_number=72,
    question_image_path="new_folder/羅桑二氏 (8).png",
    option_image_path="new_folder/羅桑二氏選項 (8).png",
    answer_value=""
)

# 練題71
graphical_question(
    page_number=73,
    question_image_path="new_folder/高級圖形一 (11).png",
    option_image_path="new_folder/高級圖形一選項 (11).png",
    answer_value=""
)
      
# 練題72
graphical_question(
    page_number=74,
    question_image_path="new_folder/高級圖形二 (16).png",
    option_image_path="new_folder/高級圖形二選項 (16).png",
    answer_value=""
)
        
# 練題73
graphical_question(
    page_number=75,
    question_image_path="new_folder/高級圖形二 (31).png",
    option_image_path="new_folder/高級圖形二選項 (31).png",
    answer_value=""
)


# 練題74
graphical_question(
    page_number=76,
    question_image_path="new_folder/高級圖形二 (12).png",
    option_image_path="new_folder/高級圖形二選項 (12).png",
    answer_value=""
)


# 練題75
graphical_question(
    page_number=77,
    question_image_path="new_folder/區分 (39).png",
    option_image_path="new_folder/區分選項 (39).png",
    answer_value=""
)

# 練題76
graphical_question(
    page_number=78,
    question_image_path="new_folder/區分 (19).png",
    option_image_path="new_folder/區分選項 (19).png",
    answer_value=""
)
    
# 練題77
graphical_question(
    page_number=79,
    question_image_path="new_folder/區分 (29).png",
    option_image_path="new_folder/區分選項 (29).png",
    answer_value=""
)

# 練題78
graphical_question(
    page_number=80,
    question_image_path="new_folder/推理思考 (17).png",
    option_image_path="new_folder/推理思考選項 (17).png",
    answer_value=""
)

# 練題79
graphical_question(
    page_number=81,
    question_image_path="new_folder/羅桑二氏 (7).png",
    option_image_path="new_folder/羅桑二氏選項 (7).png",
    answer_value=""
)

# 練題80
graphical_question(
    page_number=82,
    question_image_path="new_folder/羅桑二氏 (56).png",
    option_image_path="new_folder/羅桑二氏選項 (56).png",
    answer_value=""
)

# 練題81
graphical_question(
    page_number=83,
    question_image_path="new_folder/高級圖形一 (7).png",
    option_image_path="new_folder/高級圖形一選項 (7).png",
    answer_value=""
)
      
# 練題82
graphical_question(
    page_number=84,
    question_image_path="new_folder/高級圖形二 (22).png",
    option_image_path="new_folder/高級圖形二選項 (22).png",
    answer_value=""
)
        
# 練題83
graphical_question(
    page_number=85,
    question_image_path="new_folder/高級圖形二 (36).png",
    option_image_path="new_folder/高級圖形二選項 (36).png",
    answer_value=""
)


# 練題84
graphical_question(
    page_number=86,
    question_image_path="new_folder/高級圖形二 (24).png",
    option_image_path="new_folder/高級圖形二選項 (24).png",
    answer_value=""
)


# 練題85
graphical_question(
    page_number=87,
    question_image_path="new_folder/區分 (37).png",
    option_image_path="new_folder/區分選項 (37).png",
    answer_value=""
)

# 練題86
graphical_question(
    page_number=88,
    question_image_path="new_folder/區分 (21).png",
    option_image_path="new_folder/區分選項 (21).png",
    answer_value=""
)
    
# 練題87
graphical_question(
    page_number=89,
    question_image_path="new_folder/區分 (13).png",
    option_image_path="new_folder/區分選項 (13).png",
    answer_value=""
)

# 練題88
graphical_question(
    page_number=90,
    question_image_path="new_folder/推理思考 (1).png",
    option_image_path="new_folder/推理思考選項 (1).png",
    answer_value=""
)

# 練題89
graphical_question(
    page_number=91,
    question_image_path="new_folder/羅桑二氏 (24).png",
    option_image_path="new_folder/羅桑二氏選項 (24).png",
    answer_value=""
)

# 練題90
graphical_question(
    page_number=92,
    question_image_path="new_folder/羅桑二氏 (31).png",
    option_image_path="new_folder/羅桑二氏選項 (31).png",
    answer_value=""
)

# 練題91
graphical_question(
    page_number=93,
    question_image_path="new_folder/高級圖形一 (4).png",
    option_image_path="new_folder/高級圖形一選項 (4).png",
    answer_value=""
)
      
# 練題92
graphical_question(
    page_number=94,
    question_image_path="new_folder/高級圖形二 (7).png",
    option_image_path="new_folder/高級圖形二選項 (7).png",
    answer_value=""
)
        
# 練題93
graphical_question(
    page_number=95,
    question_image_path="new_folder/高級圖形二 (3).png",
    option_image_path="new_folder/高級圖形二選項 (3).png",
    answer_value=""
)


# 練題94
graphical_question(
    page_number=96,
    question_image_path="new_folder/高級圖形二 (2).png",
    option_image_path="new_folder/高級圖形二選項 (2).png",
    answer_value=""
)


# 練題95
graphical_question(
    page_number=97,
    question_image_path="new_folder/區分 (38).png",
    option_image_path="new_folder/區分選項 (38).png",
    answer_value=""
)

# 練題96
graphical_question(
    page_number=98,
    question_image_path="new_folder/區分 (8).png",
    option_image_path="new_folder/區分選項 (8).png",
    answer_value=""
)
    
# 練題97
graphical_question(
    page_number=99,
    question_image_path="new_folder/區分 (7).png",
    option_image_path="new_folder/區分選項 (7).png",
    answer_value=""
)

# 練題98
graphical_question(
    page_number=100,
    question_image_path="new_folder/推理思考 (9).png",
    option_image_path="new_folder/推理思考選項 (9).png",
    answer_value=""
)

# 練題99
graphical_question(
    page_number=101,
    question_image_path="new_folder/羅桑二氏 (58).png",
    option_image_path="new_folder/羅桑二氏選項 (58).png",
    answer_value=""
)

# 練題100
graphical_question(
    page_number=102,
    question_image_path="new_folder/羅桑二氏 (34).png",
    option_image_path="new_folder/羅桑二氏選項 (34).png",
    answer_value=""
)

# 練習結束後，進入過渡動畫（進度條）
if st.session_state.page == 103:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
                /* 強制整頁白底，清除殘影 */
                body, .main, .block-container {
                    background-color: white !important;
                }

                .top-container {
                    padding-top: 30px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                .stProgress {
                    width: 60%;
                    margin: 0 auto;
                }
            </style>
            <div class="top-container">
                <h4> 正在整理資料，請稍候…</h4>
            </div>
        """, unsafe_allow_html=True)

        progress_bar = st.progress(0)

    for i in range(3):  # 顯示 5 秒（0.5 秒更新一次）
        time.sleep(0.5)
        progress_bar.progress((i + 1) * 10)

    # 處理完後跳轉至第 14 頁（正式測驗前）
    st.session_state.page += 1
    st.session_state.scroll_to_top = True
    st.rerun()
    
# 顯示練習花費時間
if st.session_state.page == 104:

    # 顯示練習階段所花時間
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.session_state.get("start_time"):
            elapsed_seconds = int(time.time() - st.session_state.start_time)
            minutes = elapsed_seconds // 60
            seconds = elapsed_seconds % 60
            time_str = f"{minutes} 分 {seconds} 秒"
            st.metric(label="您在練習所花費的時間", value=time_str)
        else:
            st.warning("您未進行任何練習\n請按下一頁")
            
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    with col6:
        st.button("下一頁", on_click=next_page)

# 練習後問卷
if st.session_state.page == 105:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False

    # ✅ 強制一進來這頁就清空 warning_message（只清一次）
    if st.session_state.get("just_entered_page_15", True):
        st.session_state.warning_message = ""
        st.session_state.just_entered_page_15 = False  # 清除標記

    st.header("進入正式測驗前")
    st.markdown("---")
    st.write("（此處將放個人知覺努力程度問題說明）")

    st.markdown("""
        <style>
        .stRadio > div {
            flex-direction: row !important;
            gap: 20px; /* 調整間距 */
            flex-wrap: nowrap !important; /* 不允許換行 */
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("１. 您覺得自己有多認真對待剛才的練習題？")
        E1 = st.radio(
            label="（１=非常不認真，６=非常認真）",
            options=["1", "2", "3", "4", "5", "6"],
            key="E1", horizontal=True, index=None
        )

        st.write("２. 您覺得自己有多投入於練習階段？")
        E2 = st.radio(
            label="（１=非常不投入，６=非常投入）",
            options=["1", "2", "3", "4", "5", "6"],
            key="E2", horizontal=True, index=None
        )

        st.write("３. 您覺得自己在做練習題時有多努力？")
        E3 = st.radio(
            label="（１=非常不努力，６=非常努力）",
            options=["1", "2", "3", "4", "5", "6"],
            key="E3", horizontal=True, index=None
        )

        if st.session_state.get("warning_message"):
            st.warning(st.session_state.warning_message)

    st.markdown("---")
    spacer1, btn_col = st.columns([5, 1])

    with btn_col:
        if st.button("下一頁"):
            if st.session_state.get("E1") is None or \
               st.session_state.get("E2") is None or \
               st.session_state.get("E3") is None:
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                # ✅ 填寫完成，清除錯誤訊息，標記頁面已換
                st.session_state.warning_message = ""
                st.session_state.just_entered_page_15 = True  # 供下一頁使用
                st.session_state.page += 1
                st.rerun()

# 正式測驗時間
if "formal_start_time" not in st.session_state:
    st.session_state.formal_start_time = None

if "formal_timer_started" not in st.session_state:
    st.session_state.formal_timer_started = False

# 顯示計時器
if 106 > st.session_state.page > 112 and st.session_state.formal_timer_started:
    elapsed_seconds = int(time.time() - st.session_state.formal_start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    st.markdown(f"⏱️ **正式測驗時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 正式測驗說明
if st.session_state.page == 106:
    st.header("第二階段：正式測驗")
    st.markdown("---")
    st.write("此處將放上正式測驗說明")
    st.markdown("---")
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
                st.image(image1, caption=f"正式題 {page_number-106}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇您認為的正確圖形")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")

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
                st.image(image1, caption=f"正式題 {page_number-106}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇您認為的正確圖形")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")

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
                st.image(image1, caption=f"正式題 {page_number-106}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇您認為的正確圖形")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")

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
    page_number=107,
    question_image_path="高級圖形一 (5).png",
    option_image_path="高級圖形一選項 (5).png",
    radio_key="q_1"
)
        
# 2
question(
    page_number=108,
    question_image_path="高級圖形二 (5).png",
    option_image_path="高級圖形二選項 (5).png",
    radio_key="q_2"
)

# 3
question1(
    page_number=109,
    question_image_path="區分 (5).png",
    option_image_path="區分選項 (5).png",
    radio_key="q_3",
)

# 4
question2(
    page_number=110,
    question_image_path="推理思考 (5).png",
    option_image_path="推理思考選項 (5).png",
    radio_key="q_4"
)

# 5
question2(
    page_number=111,
    question_image_path="羅桑二氏 (5).png",
    option_image_path="羅桑二氏選項 (5).png",
    radio_key="q_5",
)

if st.session_state.page == 112:
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
    
if st.session_state.page == 113:
    st.success("測驗結果分析完成！")
    st.header("測驗結果")
    st.markdown("---")

    if st.session_state.get("formal_start_time"):
        elapsed_seconds = int(time.time() - st.session_state.formal_start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_str = f"{minutes} 分 {seconds} 秒"
    else:
        time_str = "無法取得"

    personal_score = 65
    average_score = 80

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.metric(label="您在測驗所花費的時間", value=time_str) 
    with col2:
        st.metric(label="您的分數", value=f"{personal_score}")
    with col3:
        st.metric(label="與您同齡的人的平均分數", value=f"{average_score}")

    st.markdown("---")
    # 下一頁按鈕
    col1, col2 = st.columns([5, 2])
    with col2:
        if st.button("下一頁"):
            st.session_state.page += 1
            st.session_state.scroll_to_top = True
            st.rerun()

# 操弄檢核
if st.session_state.page == 114:
    if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
    st.header("請填寫以下問題")
    st.markdown("---")
    score1 = st.text_input("您的正式測驗分數是幾分？", key="score1")
    score2 = st.text_input("同齡人平均測驗分數是幾分？", key="score2")
    comparison = st.radio("您的正式測驗分數比同齡人平均測驗分數高還是低？", ["高", "低", "不知道"], index=None, key="comparison")
  
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col2:
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    with col4:
        if st.button("下一頁"):
            if score1 is None or score2 is None or comparison is None:
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                st.session_state.warning_message = "" 
                st.session_state.page += 1
                st.rerun()

# 測驗後問卷
if st.session_state.page == 115:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("結束正式測驗前")
    st.markdown("---")
    st.write("（此處將放依變項問題說明）")

    st.write("１. 您認為自己的邏輯推理能力如何？")
    E1 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="E1", horizontal=True, index=None
    )
    
    st.write("2. 您認為自己的分析思考能力如何？")
    E2 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="E2", horizontal=True, index=None
    )

    st.write("3. 您認為自己的分析思考能力如何？")
    E3 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="E3", horizontal=True, index=None
    )
    
    if 'warning_message' in st.session_state and st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    st.markdown("---")
    spacer1, btn_col = st.columns([5, 1])

    with btn_col:
        if st.button("完成測驗"):
            if st.session_state.get("E1") is None or \
               st.session_state.get("E2") is None or \
               st.session_state.get("E3") is None:
                st.session_state.warning_message = "⚠請填寫所有問題才能繼續。"
                st.rerun()
            else:
                st.session_state.warning_message = ""
                st.session_state.page += 1
                st.rerun()

# debrief
if st.session_state.page == 116:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("實驗目的澄清")
    st.markdown("---")
    st.write("（此處將放debrief文字）")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])

    with col3:
        st.button("結束實驗", on_click=next_page)

#完成頁面
elif st.session_state.page == 117:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.success("實驗已完成！非常感謝您的參與。")
    st.balloons()
































