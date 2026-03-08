import streamlit as st
import pandas as pd
import time
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from datetime import datetime, timedelta, timezone
tz = timezone(timedelta(hours=8))

# 建立連線 (只做一次)
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# 📌 這裡只 open 一次
@st.cache_resource
def get_sheet():
    return client.open("experiment_data").worksheet("stage2-1")

sheet = get_sheet()

#初始化資料庫
for key in ["ID", "gender", "age",
            "self_esteem1", "self_esteem2", "self_esteem3", "self_esteem4", "self_esteem5"
           , "self_esteem6", "self_esteem7", "self_esteem8", "self_esteem9", "self_esteem10"
           , "mindset1", "mindset2", "mindset3", "important"
           , "Num", "E1", "E2", "E3", "E4", "E5", "score1", "score2", "comparison"
           , "prac1", "prac2", "ME1", "ME2", "ME3"
           , "SE1", "SE2", "SE3", "SE4", "SE5", "SE6", "SE7", "SE8", "SE9", "SE10" 
           , "q_1", "q_2", "q_3", "q_4", "q_5", "q_6", "q_7", "q_8", "q_9", "q_10", "q_11", "q_12", "q_13", "q_14", "q_15"
           , "q_16", "q_17"]:
    if key not in st.session_state:
        st.session_state[key] = None

# 預先設定：受試者編號 -> [允許開始時間, 允許結束時間]
participants = {
    "test00": [datetime(2025, 9, 13, 20, 30, 0, tzinfo=tz), datetime(2026, 9, 15, 21, 30, 0, tzinfo=tz)],
    "EYGT21": [datetime(2025, 9, 13, 20, 30, 0, tzinfo=tz), datetime(2026, 9, 15, 21, 30, 0, tzinfo=tz)],
    "JurM21": [datetime(2025, 9, 16, 10, 0, 0, tzinfo=tz), datetime(2026, 9, 16, 11, 0, 0, tzinfo=tz)],
    "OetM21": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2026, 9, 16, 14, 30, 0, tzinfo=tz)],
    "RaYx21": [datetime(2025, 9, 15, 14, 0, 0, tzinfo=tz), datetime(2026, 9, 15, 15, 0, 0, tzinfo=tz)],
    "ZYrQ21": [datetime(2025, 9, 16, 10, 0, 0, tzinfo=tz), datetime(2026, 9, 16, 11, 0, 0, tzinfo=tz)],
    "dFsQ21": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2026, 9, 16, 14, 30, 0, tzinfo=tz)],
    "gdFs21": [datetime(2025, 9, 15, 14, 0, 0, tzinfo=tz), datetime(2026, 9, 15, 15, 0, 0, tzinfo=tz)],
    "pXby21": [datetime(2025, 9, 16, 10, 0, 0, tzinfo=tz), datetime(2026, 9, 16, 11, 0, 0, tzinfo=tz)],
    "qfVw21": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2026, 9, 16, 14, 30, 0, tzinfo=tz)],
    "wqyA21": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2026, 9, 16, 14, 30, 0, tzinfo=tz)],
}

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
    # st.markdown(f"⏱️ **練習時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 歡迎頁
if st.session_state.page == 0:
    st.header("歡迎參加本測驗")
    st.markdown("---")
    st.write("""您好！首先非常感謝您願意參與本測驗，本測驗為政治大學心理學研究所進行的碩士學位研究。""")
    st.write("""研究目的是想要了解目前台灣學生的內隱學習能力狀況。""")
    st.write("""內隱學習能力是在近十年左右被國外研究所發現，是人內在具有的學習能力。""")
    st.write("""這個能力已被國內外研究證實，會正向影響學業及工作表現。""")
    st.write("""本測驗採用已接受過嚴格檢測的內隱學習能力測驗，共分為兩階段：練習階段與正式測驗。""")
    st.write(""" 當您開始進行本測驗，將會透過受試者編號與測驗系統連線，並在測驗完畢後顯示結果。""")
    st.write("""在測驗開始後，您有完全自主性，可以自由決定是否參與以及繼續本測驗，若您感到不適，可以隨時中止測驗。""")
    st.write("""本研究不會對您造成任何風險，您所填寫的資料將完全保密。資料收回後將由研究人員電子歸檔與保存並進行統計數據分析，預計保留5年後全數刪除，請您放心。""")
    st.write("""當您按下〔開始測驗〕表示您同意上述內容。""")
    st.write("""最後，如果您有任何疑問，可以直接聯繫研究人員（112752003@g.nccu.edu.tw）""")
    col1, col2, col3 = st.columns([1, 2, 2])
    with col3:
             st.write("""國立政治大學 心理學研究所""")
             st.write("""碩士生 游主雲""")
             st.write("""指導老師 孫蒨如 教授""")                 
    st.markdown("---")
    st.text_input("請輸入您的受試者編號", placeholder="",  key="ID")

    user_id = str(st.session_state.get("ID", "")).strip()
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col3:
             clicked = st.button("開始測驗")  # 只把按鈕放在 col3
    
    if clicked:  # 按下按鈕後才判斷
             now = datetime.now(tz)
             if user_id not in participants:
                      st.error("⚠️ 無效的受試者編號！請確認後再試。")
             else:
                      start, end = participants[user_id]
                      if start <= now <= end:
                               st.session_state["participant_id"] = user_id
                               st.session_state["start_time"] = now
                               row_data = [
                                        st.session_state.get("start_time").strftime("%Y-%m-%d %H:%M:%S"),
                                        st.session_state["ID"]
                               ]
                               sheet.append_row(row_data)
                               next_page()
                               st.rerun()
                      else:
                               st.error(f"⚠️ {user_id} 不在指定填答時間內！")


# 基本資料頁
elif st.session_state.page == 1:
    if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
    st.header("基本資料")
    st.write("以下問題是想了解您的基本資訊，以及您的一些價值觀，填寫完畢後請按〔下一頁〕進入練習階段。")
    st.markdown("---")
    st.radio("請選擇您的生理性別", ["男", "女", "其他"], horizontal=True, index=None, key="gender")
    st.selectbox("請選擇您的年齡區間", ["18-25歲", "26-35歲", "36-45歲", "46-55歲", "56-65歲", "65歲以上"], index=None, placeholder="請選擇", key="age")
    st.write("1. 我一無是處。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem1")
    st.write("2. 我有許多優點。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem2")
    st.write("3. 我能像大多數人一樣做好事情。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem3")
    st.write("4. 我沒有什麼值得驕傲的地方。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem4")
    st.write("5. 我很沒用。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem5")
    st.write("6. 我是一個有價值的人。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem6")
    st.write("7. 我希望我能更尊重自己。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem7")
    st.write("8. 整體來說，我是個失敗者。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem8")
    st.write("9. 我對自己抱持正面的態度。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem9")
    st.write("10. 整體來說，我對自己感到滿意。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="self_esteem10")
    st.write("11. 人的聰明程度是固定的，無論做什麼都不能改變。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="mindset1")
    st.write("12. 人可以學新的東西，但沒有辦法真正改變自己原本的聰明程度。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="mindset2")
    st.write("13. 一個人有多聰明是不能夠改變的。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="mindset3")
    st.write("14. 內隱學習能力是重要的。")
    st.radio("（１=非常不同意，６=非常同意）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="important")
    # st.write("15. 對您來說，分析思考能力有多重要？")
    # st.radio("（１=非常不重要，６=非常重要）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="important2")
    # st.write("16. 對您來說，圖形理解能力有多重要？")
    # st.radio("（１=非常不重要，６=非常重要）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="important3")

    st.markdown("---")


    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col2:
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    with col4:
             warning_needed = False
             if st.button("下一頁"):
                      if (st.session_state.get("gender") is None or st.session_state.get("age") is None 
                          or st.session_state.get("self_esteem1") is None or st.session_state.get("self_esteem2") is None 
                          or st.session_state.get("self_esteem3") is None or st.session_state.get("self_esteem4") is None 
                          or st.session_state.get("self_esteem5") is None or st.session_state.get("self_esteem6") is None 
                          or st.session_state.get("self_esteem7") is None or st.session_state.get("self_esteem8") is None 
                          or st.session_state.get("self_esteem9") is None or st.session_state.get("self_esteem10") is None 
                          or st.session_state.get("mindset1") is None or st.session_state.get("mindset2") is None 
                          or st.session_state.get("mindset3") is None or st.session_state.get("important") is None):
                                   warning_needed = True
                      else:
                               row_data = [st.session_state["ID"],
                                        st.session_state["ID"], st.session_state["gender"], st.session_state["age"],
                                        st.session_state["self_esteem1"], st.session_state["self_esteem2"],
                                        st.session_state["self_esteem3"], st.session_state["self_esteem4"],
                                        st.session_state["self_esteem5"], st.session_state["self_esteem6"],
                                        st.session_state["self_esteem7"], st.session_state["self_esteem8"],
                                        st.session_state["self_esteem9"], st.session_state["self_esteem10"],
                                        st.session_state["mindset1"], st.session_state["mindset2"], st.session_state["mindset3"],
                                        st.session_state["important"]  
                               ]
                               sheet.append_row(row_data)
                               next_page() 
                               st.rerun()
    if warning_needed: st.warning("⚠️ 請填寫所有問題才能繼續。")

# 練習說明
elif st.session_state.page == 2:
    st.header("第一階段：練習測驗")
    st.markdown("---")
    st.write("""歡迎您來到練習階段！""")
    st.write("""為了幫助您了解正式測驗的題型，本階段設有多道練習題。""")
    st.write("""過去很多研究發現在本階段越努力的受試者，在正式測驗的表現結果越好。""")
    st.write("""在本階段的努力程度指的是練習時間長度與練習題數。""")
    st.write("""建議您練習【11~16題】後，就可以點選〔直接進入正式測驗〕。""")
    st.write("""但本研究不強制規定您的練習題數，您仍可以自由選擇。""") 
    st.write("""＊每一題都請認真思考後再看答案。""") 
    st.write("""了解以上說明後，請您按下〔開始練習〕進入練習階段。""")
    st.write("""（提醒：畫面閃爍實屬正常，請別擔心！）""")
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
    with col3:
        if st.button("開始練習"):
            st.session_state.start_time = time.time()
            st.session_state.timer_started = True
            st.session_state.page += 1  # 進入下一頁
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
                st.image(image2, caption="請選擇符合題目規律的圖形")
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
                st.session_state.page = 103
                st.session_state.scroll_to_top = True
                st.rerun()
    
# 練題1
graphical_question(
    page_number=3,
    question_image_path="new_folder/高級圖形一 (3).png",
    option_image_path="new_folder/高級圖形一選項 (3).png",
    answer_value="5"
)
      
# 練題2
graphical_question(
    page_number=4,
    question_image_path="new_folder/高級圖形二 (19).png",
    option_image_path="new_folder/高級圖形二選項 (19).png",
    answer_value="2"
)
        
# 練題3
graphical_question(
    page_number=5,
    question_image_path="new_folder/高級圖形二 (18).png",
    option_image_path="new_folder/高級圖形二選項 (18).png",
    answer_value="7"
)


# 練題4
graphical_question(
    page_number=6,
    question_image_path="new_folder/高級圖形二 (23).png",
    option_image_path="new_folder/高級圖形二選項 (23).png",
    answer_value="5"
)


# 練題5
graphical_question(
    page_number=7,
    question_image_path="new_folder/區分 (24).png",
    option_image_path="new_folder/區分選項 (24).png",
    answer_value="B"
)

# 練題6
graphical_question(
    page_number=8,
    question_image_path="new_folder/區分 (4).png",
    option_image_path="new_folder/區分選項 (4).png",
    answer_value="B"
)
    
# 練題7
graphical_question(
    page_number=9,
    question_image_path="new_folder/區分 (18).png",
    option_image_path="new_folder/區分選項 (18).png",
    answer_value="C"
)

# 練題8
graphical_question(
    page_number=10,
    question_image_path="new_folder/推理思考 (8).png",
    option_image_path="new_folder/推理思考選項 (8).png",
    answer_value="2"
)

# 練題9
graphical_question(
    page_number=11,
    question_image_path="new_folder/羅桑二氏 (51).png",
    option_image_path="new_folder/羅桑二氏選項 (51).png",
    answer_value="3"
)

# 練題10
graphical_question(
    page_number=12,
    question_image_path="new_folder/羅桑二氏 (16).png",
    option_image_path="new_folder/羅桑二氏選項 (16).png",
    answer_value="3"
)

# 練題11
graphical_question(
    page_number=13,
    question_image_path="new_folder/高級圖形一 (8).png",
    option_image_path="new_folder/高級圖形一選項 (8).png",
    answer_value="3"
)
      
# 練題12
graphical_question(
    page_number=14,
    question_image_path="new_folder/高級圖形二 (28).png",
    option_image_path="new_folder/高級圖形二選項 (28).png",
    answer_value="3"
)
        
# 練題13
graphical_question(
    page_number=15,
    question_image_path="new_folder/高級圖形二 (32).png",
    option_image_path="new_folder/高級圖形二選項 (32).png",
    answer_value="7"
)


# 練題14
graphical_question(
    page_number=16,
    question_image_path="new_folder/區分 (17).png",
    option_image_path="new_folder/區分選項 (17).png",
    answer_value="E"
)


# 練題15
graphical_question(
    page_number=17,
    question_image_path="new_folder/區分 (14).png",
    option_image_path="new_folder/區分選項 (14).png",
    answer_value="D"
)

# 練題16
graphical_question(
    page_number=18,
    question_image_path="new_folder/區分 (12).png",
    option_image_path="new_folder/區分選項 (12).png",
    answer_value="B"
)
    
# 練題17
graphical_question(
    page_number=19,
    question_image_path="new_folder/推理思考 (6).png",
    option_image_path="new_folder/推理思考選項 (6).png",
    answer_value="2"
)

# 練題18
graphical_question(
    page_number=20,
    question_image_path="new_folder/推理思考 (11).png",
    option_image_path="new_folder/推理思考選項 (11).png",
    answer_value="4"
)

# 練題19
graphical_question(
    page_number=21,
    question_image_path="new_folder/羅桑二氏 (3).png",
    option_image_path="new_folder/羅桑二氏選項 (3).png",
    answer_value="5"
)

# 練題20
graphical_question(
    page_number=22,
    question_image_path="new_folder/羅桑二氏 (47).png",
    option_image_path="new_folder/羅桑二氏選項 (47).png",
    answer_value="4"
)

# 練題21
graphical_question(
    page_number=23,
    question_image_path="new_folder/高級圖形一 (2).png",
    option_image_path="new_folder/高級圖形一選項 (2).png",
    answer_value="4"
)
      
# 練題22
graphical_question(
    page_number=24,
    question_image_path="new_folder/高級圖形二 (21).png",
    option_image_path="new_folder/高級圖形二選項 (21).png",
    answer_value="5"
)
        
# 練題23
graphical_question(
    page_number=25,
    question_image_path="new_folder/高級圖形二 (4).png",
    option_image_path="new_folder/高級圖形二選項 (4).png",
    answer_value="5"
)


# 練題24
graphical_question(
    page_number=26,
    question_image_path="new_folder/區分 (23).png",
    option_image_path="new_folder/區分選項 (23).png",
    answer_value="A"
)


# 練題25
graphical_question(
    page_number=27,
    question_image_path="new_folder/區分 (32).png",
    option_image_path="new_folder/區分選項 (32).png",
    answer_value="E"
)

# 練題26
graphical_question(
    page_number=28,
    question_image_path="new_folder/區分 (11).png",
    option_image_path="new_folder/區分選項 (11).png",
    answer_value="A"
)
    
# 練題27
graphical_question(
    page_number=29,
    question_image_path="new_folder/推理思考 (12).png",
    option_image_path="new_folder/推理思考選項 (12).png",
    answer_value="4"
)

# 練題28
graphical_question(
    page_number=30,
    question_image_path="new_folder/推理思考 (13).png",
    option_image_path="new_folder/推理思考選項 (13).png",
    answer_value="2"
)

# 練題29
graphical_question(
    page_number=31,
    question_image_path="new_folder/羅桑二氏 (33).png",
    option_image_path="new_folder/羅桑二氏選項 (33).png",
    answer_value="5"
)

# 練題30
graphical_question(
    page_number=32,
    question_image_path="new_folder/羅桑二氏 (54).png",
    option_image_path="new_folder/羅桑二氏選項 (54).png",
    answer_value="1"
)

# 練題31
graphical_question(
    page_number=33,
    question_image_path="new_folder/高級圖形一 (6).png",
    option_image_path="new_folder/高級圖形一選項 (6).png",
    answer_value="5"
)
      
# 練題32
graphical_question(
    page_number=34,
    question_image_path="new_folder/高級圖形二 (26).png",
    option_image_path="new_folder/高級圖形二選項 (26).png",
    answer_value="5"
)
        
# 練題33
graphical_question(
    page_number=35,
    question_image_path="new_folder/高級圖形二 (13).png",
    option_image_path="new_folder/高級圖形二選項 (13).png",
    answer_value="8"
)


# 練題34
graphical_question(
    page_number=36,
    question_image_path="new_folder/高級圖形二 (9).png",
    option_image_path="new_folder/高級圖形二選項 (9).png",
    answer_value="4"
)


# 練題35
graphical_question(
    page_number=37,
    question_image_path="new_folder/區分 (16).png",
    option_image_path="new_folder/區分選項 (16).png",
    answer_value="C"
)

# 練題36
graphical_question(
    page_number=38,
    question_image_path="new_folder/區分 (31).png",
    option_image_path="new_folder/區分選項 (31).png",
    answer_value="B"
)
    
# 練題37
graphical_question(
    page_number=39,
    question_image_path="new_folder/區分 (27).png",
    option_image_path="new_folder/區分選項 (27).png",
    answer_value="E"
)

# 練題38
graphical_question(
    page_number=40,
    question_image_path="new_folder/推理思考 (14).png",
    option_image_path="new_folder/推理思考選項 (14).png",
    answer_value="4"
)

# 練題39
graphical_question(
    page_number=41,
    question_image_path="new_folder/羅桑二氏 (59).png",
    option_image_path="new_folder/羅桑二氏選項 (59).png",
    answer_value="2"
)

# 練題40
graphical_question(
    page_number=42,
    question_image_path="new_folder/羅桑二氏 (57).png",
    option_image_path="new_folder/羅桑二氏選項 (57).png",
    answer_value="4"
)

# 練題41
graphical_question(
    page_number=43,
    question_image_path="new_folder/高級圖形一 (9).png",
    option_image_path="new_folder/高級圖形一選項 (9).png",
    answer_value="7"
)
      
# 練題42
graphical_question(
    page_number=44,
    question_image_path="new_folder/高級圖形二 (29).png",
    option_image_path="new_folder/高級圖形二選項 (29).png",
    answer_value="2"
)
        
# 練題43
graphical_question(
    page_number=45,
    question_image_path="new_folder/高級圖形二 (34).png",
    option_image_path="new_folder/高級圖形二選項 (34).png",
    answer_value="3"
)


# 練題44
graphical_question(
    page_number=46,
    question_image_path="new_folder/高級圖形二 (17).png",
    option_image_path="new_folder/高級圖形二選項 (17).png",
    answer_value="3"
)


# 練題45
graphical_question(
    page_number=47,
    question_image_path="new_folder/區分 (34).png",
    option_image_path="new_folder/區分選項 (34).png",
    answer_value="E"
)

# 練題46
graphical_question(
    page_number=48,
    question_image_path="new_folder/區分 (1).png",
    option_image_path="new_folder/區分選項 (1).png",
    answer_value="E"
)
    
# 練題47
graphical_question(
    page_number=49,
    question_image_path="new_folder/區分 (9).png",
    option_image_path="new_folder/區分選項 (9).png",
    answer_value="C"
)

# 練題48
graphical_question(
    page_number=50,
    question_image_path="new_folder/推理思考 (16).png",
    option_image_path="new_folder/推理思考選項 (16).png",
    answer_value="5"
)

# 練題49
graphical_question(
    page_number=51,
    question_image_path="new_folder/羅桑二氏 (36).png",
    option_image_path="new_folder/羅桑二氏選項 (36).png",
    answer_value="3"
)

# 練題50
graphical_question(
    page_number=52,
    question_image_path="new_folder/羅桑二氏 (18).png",
    option_image_path="new_folder/羅桑二氏選項 (18).png",
    answer_value="1"
)

# 練題51
graphical_question(
    page_number=53,
    question_image_path="new_folder/高級圖形一 (1).png",
    option_image_path="new_folder/高級圖形一選項 (1).png",
    answer_value="8"
)
      
# 練題52
graphical_question(
    page_number=54,
    question_image_path="new_folder/高級圖形二 (8).png",
    option_image_path="new_folder/高級圖形二選項 (8).png",
    answer_value="2"
)
        
# 練題53
graphical_question(
    page_number=55,
    question_image_path="new_folder/高級圖形二 (33).png",
    option_image_path="new_folder/高級圖形二選項 (33).png",
    answer_value="4"
)


# 練題54
graphical_question(
    page_number=56,
    question_image_path="new_folder/區分 (3).png",
    option_image_path="new_folder/區分選項 (3).png",
    answer_value="B"
)


# 練題55
graphical_question(
    page_number=57,
    question_image_path="new_folder/區分 (36).png",
    option_image_path="new_folder/區分選項 (36).png",
    answer_value="D"
)

# 練題56
graphical_question(
    page_number=58,
    question_image_path="new_folder/區分 (22).png",
    option_image_path="new_folder/區分選項 (22).png",
    answer_value="E"
)
    
# 練題57
graphical_question(
    page_number=59,
    question_image_path="new_folder/推理思考 (18).png",
    option_image_path="new_folder/推理思考選項 (18).png",
    answer_value="5"
)

# 練題58
graphical_question(
    page_number=60,
    question_image_path="new_folder/推理思考 (3).png",
    option_image_path="new_folder/推理思考選項 (3).png",
    answer_value="3"
)

# 練題59
graphical_question(
    page_number=61,
    question_image_path="new_folder/羅桑二氏 (19).png",
    option_image_path="new_folder/羅桑二氏選項 (19).png",
    answer_value="5"
)

# 練題60
graphical_question(
    page_number=62,
    question_image_path="new_folder/羅桑二氏 (45).png",
    option_image_path="new_folder/羅桑二氏選項 (45).png",
    answer_value="3"
)

# 練題61
graphical_question(
    page_number=63,
    question_image_path="new_folder/高級圖形一 (12).png",
    option_image_path="new_folder/高級圖形一選項 (12).png",
    answer_value="7"
)
      
# 練題62
graphical_question(
    page_number=64,
    question_image_path="new_folder/高級圖形二 (14).png",
    option_image_path="new_folder/高級圖形二選項 (14).png",
    answer_value="8"
)
        
# 練題63
graphical_question(
    page_number=65,
    question_image_path="new_folder/高級圖形二 (27).png",
    option_image_path="new_folder/高級圖形二選項 (27).png",
    answer_value="1"
)


# 練題64
graphical_question(
    page_number=66,
    question_image_path="new_folder/區分 (33).png",
    option_image_path="new_folder/區分選項 (33).png",
    answer_value="D"
)


# 練題65
graphical_question(
    page_number=67,
    question_image_path="new_folder/區分 (2).png",
    option_image_path="new_folder/區分選項 (2).png",
    answer_value="B"
)

# 練題66
graphical_question(
    page_number=68,
    question_image_path="new_folder/區分 (6).png",
    option_image_path="new_folder/區分選項 (6).png",
    answer_value="B"
)
    
# 練題67
graphical_question(
    page_number=69,
    question_image_path="new_folder/推理思考 (19).png",
    option_image_path="new_folder/推理思考選項 (19).png",
    answer_value="3"
)

# 練題68
graphical_question(
    page_number=70,
    question_image_path="new_folder/推理思考 (4).png",
    option_image_path="new_folder/推理思考選項 (4).png",
    answer_value="3"
)

# 練題69
graphical_question(
    page_number=71,
    question_image_path="new_folder/羅桑二氏 (25).png",
    option_image_path="new_folder/羅桑二氏選項 (25).png",
    answer_value="3"
)

# 練題70
graphical_question(
    page_number=72,
    question_image_path="new_folder/羅桑二氏 (8).png",
    option_image_path="new_folder/羅桑二氏選項 (8).png",
    answer_value="5"
)

# 練題71
graphical_question(
    page_number=73,
    question_image_path="new_folder/高級圖形一 (11).png",
    option_image_path="new_folder/高級圖形一選項 (11).png",
    answer_value="6"
)
      
# 練題72
graphical_question(
    page_number=74,
    question_image_path="new_folder/高級圖形二 (16).png",
    option_image_path="new_folder/高級圖形二選項 (16).png",
    answer_value="6"
)
        
# 練題73
graphical_question(
    page_number=75,
    question_image_path="new_folder/高級圖形二 (31).png",
    option_image_path="new_folder/高級圖形二選項 (31).png",
    answer_value="1"
)


# 練題74
graphical_question(
    page_number=76,
    question_image_path="new_folder/高級圖形二 (12).png",
    option_image_path="new_folder/高級圖形二選項 (12).png",
    answer_value="3"
)


# 練題75
graphical_question(
    page_number=77,
    question_image_path="new_folder/區分 (39).png",
    option_image_path="new_folder/區分選項 (39).png",
    answer_value="E"
)

# 練題76
graphical_question(
    page_number=78,
    question_image_path="new_folder/區分 (19).png",
    option_image_path="new_folder/區分選項 (19).png",
    answer_value="C"
)
    
# 練題77
graphical_question(
    page_number=79,
    question_image_path="new_folder/區分 (29).png",
    option_image_path="new_folder/區分選項 (29).png",
    answer_value="D"
)

# 練題78
graphical_question(
    page_number=80,
    question_image_path="new_folder/推理思考 (17).png",
    option_image_path="new_folder/推理思考選項 (17).png",
    answer_value="1"
)

# 練題79
graphical_question(
    page_number=81,
    question_image_path="new_folder/羅桑二氏 (7).png",
    option_image_path="new_folder/羅桑二氏選項 (7).png",
    answer_value="2"
)

# 練題80
graphical_question(
    page_number=82,
    question_image_path="new_folder/羅桑二氏 (56).png",
    option_image_path="new_folder/羅桑二氏選項 (56).png",
    answer_value="4"
)

# 練題81
graphical_question(
    page_number=83,
    question_image_path="new_folder/高級圖形一 (7).png",
    option_image_path="new_folder/高級圖形一選項 (7).png",
    answer_value="6"
)
      
# 練題82
graphical_question(
    page_number=84,
    question_image_path="new_folder/高級圖形二 (22).png",
    option_image_path="new_folder/高級圖形二選項 (22).png",
    answer_value="6"
)
        
# 練題83
graphical_question(
    page_number=85,
    question_image_path="new_folder/高級圖形二 (36).png",
    option_image_path="new_folder/高級圖形二選項 (36).png",
    answer_value="6"
)


# 練題84
graphical_question(
    page_number=86,
    question_image_path="new_folder/高級圖形二 (24).png",
    option_image_path="new_folder/高級圖形二選項 (24).png",
    answer_value="4"
)


# 練題85
graphical_question(
    page_number=87,
    question_image_path="new_folder/區分 (37).png",
    option_image_path="new_folder/區分選項 (37).png",
    answer_value="D"
)

# 練題86
graphical_question(
    page_number=88,
    question_image_path="new_folder/區分 (21).png",
    option_image_path="new_folder/區分選項 (21).png",
    answer_value="C"
)
    
# 練題87
graphical_question(
    page_number=89,
    question_image_path="new_folder/區分 (13).png",
    option_image_path="new_folder/區分選項 (13).png",
    answer_value="C"
)

# 練題88
graphical_question(
    page_number=90,
    question_image_path="new_folder/推理思考 (1).png",
    option_image_path="new_folder/推理思考選項 (1).png",
    answer_value="4"
)

# 練題89
graphical_question(
    page_number=91,
    question_image_path="new_folder/羅桑二氏 (24).png",
    option_image_path="new_folder/羅桑二氏選項 (24).png",
    answer_value="4"
)

# 練題90
graphical_question(
    page_number=92,
    question_image_path="new_folder/羅桑二氏 (31).png",
    option_image_path="new_folder/羅桑二氏選項 (31).png",
    answer_value="1"
)

# 練題91
graphical_question(
    page_number=93,
    question_image_path="new_folder/高級圖形一 (4).png",
    option_image_path="new_folder/高級圖形一選項 (4).png",
    answer_value="1"
)
      
# 練題92
graphical_question(
    page_number=94,
    question_image_path="new_folder/高級圖形二 (7).png",
    option_image_path="new_folder/高級圖形二選項 (7).png",
    answer_value="1"
)
        
# 練題93
graphical_question(
    page_number=95,
    question_image_path="new_folder/高級圖形二 (3).png",
    option_image_path="new_folder/高級圖形二選項 (3).png",
    answer_value="4"
)


# 練題94
graphical_question(
    page_number=96,
    question_image_path="new_folder/高級圖形二 (2).png",
    option_image_path="new_folder/高級圖形二選項 (2).png",
    answer_value="8"
)


# 練題95
graphical_question(
    page_number=97,
    question_image_path="new_folder/區分 (38).png",
    option_image_path="new_folder/區分選項 (38).png",
    answer_value="B"
)

# 練題96
graphical_question(
    page_number=98,
    question_image_path="new_folder/區分 (8).png",
    option_image_path="new_folder/區分選項 (8).png",
    answer_value="B"
)
    
# 練題97
graphical_question(
    page_number=99,
    question_image_path="new_folder/區分 (7).png",
    option_image_path="new_folder/區分選項 (7).png",
    answer_value="B"
)

# 練題98
graphical_question(
    page_number=100,
    question_image_path="new_folder/推理思考 (9).png",
    option_image_path="new_folder/推理思考選項 (9).png",
    answer_value="1"
)

# 練題99
graphical_question(
    page_number=101,
    question_image_path="new_folder/羅桑二氏 (58).png",
    option_image_path="new_folder/羅桑二氏選項 (58).png",
    answer_value="2"
)

# 練題100
graphical_question(
    page_number=102,
    question_image_path="new_folder/羅桑二氏 (34).png",
    option_image_path="new_folder/羅桑二氏選項 (34).png",
    answer_value="4"
)
                
# 正式測驗說明
if st.session_state.page == 103:
    st.header("第二階段：正式測驗")
    st.markdown("---")
    st.write("""歡迎您來到正式測驗！請完整閱讀以下說明：""")
    st.write("""本階段共有17道正式測驗題，測驗期間不得使用任何方式查詢答案。""")
    st.write("""測驗結束後將由系統透過您的【答題時間與正確率】計算您的測驗分數。""")
    st.write("""請您務必認真作答，確保分數的有效性。""")
    st.write("""提醒您，每題僅能作答一次，無法更改答案或回到上一頁，因此請您確認答案後再到下一題。""")
    st.write("""了解以上說明後，請您按下〔開始測驗〕進入正式測驗。""")
    st.write("""（提醒：畫面閃爍實屬正常，請別擔心！）""")
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
                st.image(image1, caption=f"正式題 {page_number-104}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇符合題目規律的圖形")
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

        # with col1:
        #     st.button("上一頁", on_click=prev_page)

        with col6:
            if st.button("下一頁"):
                if st.session_state.get(radio_key) is None:
                    warning_needed = True  # 觸發提示
                else:
                         row_data = [st.session_state.get(radio_key)]
                         sheet.append_row(row_data)
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
                st.image(image1, caption=f"正式題 {page_number-104}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇符合題目規律的圖形")
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

        # with col1:
        #     st.button("上一頁", on_click=prev_page)

        with col6:
            if st.button("下一頁"):
                if st.session_state.get(radio_key) is None:
                    warning_needed = True  # 觸發提示
                else:
                         row_data = [st.session_state.get(radio_key)]
                         sheet.append_row(row_data)
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
                st.image(image1, caption=f"正式題 {page_number-104}")
            except FileNotFoundError:
                st.warning("⚠️ 圖片載入失敗")
        
        with col2:
            try:
                image2 = Image.open(option_image_path)
                st.image(image2, caption="請選擇符合題目規律的圖形")
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

        with col6:
            if st.button("下一頁"):
                if st.session_state.get(radio_key) is None:
                    warning_needed = True  # 觸發提示
                else:
                         row_data = [st.session_state.get(radio_key)]
                         sheet.append_row(row_data)
                         next_page()
                         st.rerun()
        
        if warning_needed:
            st.warning("⚠️ 請先作答才能繼續。")


# 1
question(
    page_number=104,
    question_image_path="new_folder/高級圖形一 (5).png",
    option_image_path="new_folder/高級圖形一選項 (5).png",
    radio_key="q_1"
)
        
# 2
question(
    page_number=105,
    question_image_path="new_folder/高級圖形二 (11).png",
    option_image_path="new_folder/高級圖形二選項 (11).png",
    radio_key="q_2"
)

# 3
question(
    page_number=106,
    question_image_path="new_folder/高級圖形二 (15).png",
    option_image_path="new_folder/高級圖形二選項 (15).png",
    radio_key="q_3",
)

# 4
question1(
    page_number=107,
    question_image_path="new_folder/區分 (20).png",
    option_image_path="new_folder/區分選項 (20).png",
    radio_key="q_4"
)

# 5
question1(
    page_number=108,
    question_image_path="new_folder/區分 (5).png",
    option_image_path="new_folder/區分選項 (5).png",
    radio_key="q_5",
)

# 6
question1(
    page_number=109,
    question_image_path="new_folder/區分 (40).png",
    option_image_path="new_folder/區分選項 (40).png",
    radio_key="q_6",
)

# 7
question2(
    page_number=110,
    question_image_path="new_folder/推理思考 (5).png",
    option_image_path="new_folder/推理思考選項 (5).png",
    radio_key="q_7",
)

# 8
question2(
    page_number=111,
    question_image_path="new_folder/羅桑二氏 (50).png",
    option_image_path="new_folder/羅桑二氏選項 (50).png",
    radio_key="q_8",
)

# 9
question2(
    page_number=112,
    question_image_path="new_folder/羅桑二氏 (30).png",
    option_image_path="new_folder/羅桑二氏選項 (30).png",
    radio_key="q_9",
)

# 10
question2(
    page_number=113,
    question_image_path="new_folder/羅桑二氏 (55).png",
    option_image_path="new_folder/羅桑二氏選項 (55).png",
    radio_key="q_10",
)

# 11
question(
    page_number=114,
    question_image_path="new_folder/高級圖形二 (20).png",
    option_image_path="new_folder/高級圖形二選項 (20).png",
    radio_key="q_11"
)

# 12
question(
    page_number=115,
    question_image_path="new_folder/高級圖形二 (5).png",
    option_image_path="new_folder/高級圖形二選項 (5).png",
    radio_key="q_12",
)

# 13
question1(
    page_number=116,
    question_image_path="new_folder/區分 (25).png",
    option_image_path="new_folder/區分選項 (25).png",
    radio_key="q_13"
)

# 14
question1(
    page_number=117,
    question_image_path="new_folder/區分 (30).png",
    option_image_path="new_folder/區分選項 (30).png",
    radio_key="q_14",
)

# 15
question1(
    page_number=118,
    question_image_path="new_folder/區分 (35).png",
    option_image_path="new_folder/區分選項 (35).png",
    radio_key="q_15",
)

# 16
question2(
    page_number=119,
    question_image_path="new_folder/推理思考 (7).png",
    option_image_path="new_folder/推理思考選項 (7).png",
    radio_key="q_16",
)

# 17
question2(
    page_number=120,
    question_image_path="new_folder/高級圖形二 (25).png",
    option_image_path="new_folder/高級圖形二選項 (25).png",
    radio_key="q_17",
)

if st.session_state.page == 121:
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("### ⏳ 分數計算中，請稍候…")
         
    # 在頁面最後放一個 container
    bottom_placeholder = st.container()
    with bottom_placeholder:
        progress_bar = st.progress(0)

    for i in range(10):
        time.sleep(0.5)
        progress_bar.progress((i + 1) * 10)

    st.markdown("### ⏳ 資料處理中，請稍候…")

    # 在頁面最後放一個 container
    bottom_placeholder = st.container()
    with bottom_placeholder:
        progress_bar = st.progress(0)

    for i in range(10):
        time.sleep(0.5)
        progress_bar.progress((i + 1) * 10)

    st.session_state.page += 1
    st.session_state.scroll_to_top = True
    st.rerun()
    
if st.session_state.page == 122:
    st.success("測驗結果分析完成！")
    st.header("測驗結果")
    st.markdown("---")

    personal_score = 65
    average_score = 80
    Img = Image.open("new_folder/圖片1.png")

    import re
    p_time = sheet.acell("S4").value 
    match = re.match(r"(\d+)分(\d+)秒", p_time)
    minutes = int(match.group(1))
    seconds = int(match.group(2))
    total_seconds = minutes * 60 + seconds
    new_seconds = total_seconds / 2 + 25
    new_seconds = int(new_seconds)
    new_min = new_seconds // 60
    new_sec = new_seconds % 60
    avg_time = f"{new_min}分{new_sec}秒"

    st.write("""以下是您與同齡人們在練習階段所花費的練習時間。""")     
    col1, col2 = st.columns([1, 1]) 
    with col1:
             st.metric(label="您先前的練習時間", value=sheet.acell("S4").value")  
    with col2:
             st.metric(label="同齡人們的平均練習時間", value=avg_time)  

    st.write("""以下是您與同齡人們在正式測驗所得到的分數。""")     
    col1, col2, col3 = st.columns([1, 1, 2]) 
    with col1:
             st.metric(label="您的分數", value=f"{personal_score} 分") 
             
    with col2:
             st.metric(label="同齡人平均分數", value=f"{average_score} 分") 
     
    with col3:
             st.image(Img)
        
    st.markdown("---")
    # 下一頁按鈕
    col1, col2 = st.columns([5, 2])
    with col2:
        if st.button("下一頁"):
            st.session_state.page += 1
            st.session_state.scroll_to_top = True
            st.rerun()

# 操弄檢核
if st.session_state.page == 123:
    if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
    st.header("測驗結束前")
    st.markdown("---")
    st.write("""以下問題是想了解您的練習狀況與測驗結果。填寫完畢後請按〔下一頁〕。""")
    prac1 = st.text_input("您比同齡人練習的時間更多還是更少？", ["更多", "更少", "差不多一樣多"], index=None, key="prac1")
    prac2 = st.text_input("您認為誰在練習階段更努力？", ["自己", "同齡人們", "差不多一樣努力"], index=None, key="prac2")
    score1 = st.text_input("您的正式測驗分數是幾分？", placeholder="請輸入數字",  key="score1")
    score2 = st.text_input("同齡人平均測驗分數是幾分？", placeholder="請輸入數字", key="score2")
    comparison = st.radio("您的正式測驗分數比同齡人平均測驗分數高還是低？", ["高", "低", "不知道"], index=None, key="comparison")
    
    st.write("１. 您認為自己是否有可能（有機會）得到和同齡人們一樣的分數？")
    ME1 = st.radio(
        label="（１=非常不可能，６=非常可能）",
        options=["1", "2", "3", "4", "5", "6"],
        key="ME1", horizontal=True, index=None)
    st.write("２. 您是否有信心得到和同齡人們一樣的分數？")
    ME2 = st.radio(
        label="（１=非常沒信心，６=非常有信心）",
        options=["1", "2", "3", "4", "5", "6"],
        key="ME2", horizontal=True, index=None)
    st.write("３. 要得到和同齡人們一樣的分數，對您來說是否困難？")
    ME3 = st.radio(
        label="（１=非常不困難，６=非常困難）",
        options=["1", "2", "3", "4", "5", "6"],
        key="ME3", horizontal=True, index=None)
         
         
    # 加上 JS/HTML 把 autocomplete 關掉
    st.markdown("""
    <style>
    input[type="text"] {
    autocomplete: off;
    }
    </style>
    """, unsafe_allow_html=True)
  
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col2:
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)

    with col4:
        if st.button("下一頁"):
            if prac1 is None or prac2 is None or score1 is None or score2 is None or comparison is None
                 or ME1 is None or ME2 is None or ME3 is None:
                st.session_state.warning_message = "⚠️ 請填寫所有問題才能繼續。"
                st.rerun()
            else:
                     row_data = [st.session_state["ID"],
                              st.session_state["ID"], st.session_state["gender"], st.session_state["age"],
                              st.session_state["self_esteem1"], st.session_state["self_esteem2"],
                              st.session_state["self_esteem3"], st.session_state["self_esteem4"],
                              st.session_state["self_esteem5"], st.session_state["self_esteem6"],
                              st.session_state["self_esteem7"], st.session_state["self_esteem8"],
                              st.session_state["self_esteem9"], st.session_state["self_esteem10"],
                              st.session_state["mindset1"], st.session_state["mindset2"], st.session_state["mindset3"],
                              st.session_state["important"], st.session_state["important"], st.session_state["important"], 
                              st.session_state["prac1"], st.session_state["prac2"],
                              st.session_state["score1"], st.session_state["score2"], st.session_state["comparison"],
                              st.session_state["ME1"], st.session_state["ME2"], st.session_state["ME3"],
                     ]
                     sheet.append_row(row_data)
                     st.session_state.warning_message = "" 
                     st.session_state.page += 1
                     st.rerun()

# 測驗後問卷
if st.session_state.page == 124:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("結束本測驗前")
    st.markdown("---")
    st.write("""以下問題是想了解您的一些想法。填寫完畢後請按〔完成測驗〕。""")

    st.write("１. 您認為自己的內隱學習能力如何？")
    SE1 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE1", horizontal=True, index=None)

    st.write("２. 您對自己的內隱學習能力有多少信心？")
    SE2 = st.radio(
        label="（１=非常沒信心，６=非常有信心）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE2", horizontal=True, index=None)

    st.write("３. 您認為自己在正式測驗的表現如何？")
    SE3 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE3", horizontal=True, index=None)
    
    st.write("４. 若再進行一次測驗，您認為自己的表現會如何？")
    SE4 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE4", horizontal=True, index=None)

    st.write("５. 您對自己的正式測驗表現結果有多滿意？")
    SE5 = st.radio(
        label="（１=非常不滿意，６=非常滿意）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE5", horizontal=True, index=None)

    st.write("６. 您看到正式測驗的分數後有多愉快？")
    SE6 = st.radio(
        label="（１=非常不愉快，６=非常愉快）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE6", horizontal=True, index=None)
         
    st.write("７. 您認為本測驗能正確測量到您內隱學習能力的程度？")
    SE7 = st.radio(
        label="（１=非常不正確，６=非常正確）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE7", horizontal=True, index=None)
    
    st.write("８. 您是否同意本測驗的內容是有效的？")
    SE8 = st.radio(
        label="（１=非常不同意，６=非常同意）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE8", horizontal=True, index=None)
         
    st.write("９. 您認為自己在正式測驗有多認真？")
    SE9 = st.radio(
             label="（１=非常不認真，６=非常認真）",
             options=["1", "2", "3", "4", "5", "6"],
             key="SE9", horizontal=True, index=None)
    
    st.write("１０. 您有多投入於正式測驗？")
    SE10 = st.radio(
             label="（１=非常不投入，６=非常投入）",
             options=["1", "2", "3", "4", "5", "6"],
             key="SE10", horizontal=True, index=None)
    
    if 'warning_message' in st.session_state and st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    st.markdown("---")
    spacer1, spacer2, btn_col, spacer3 = st.columns([1, 1, 2, 1])

    with btn_col:
        warning_needed = False
        if st.button("完成測驗"):
            if st.session_state.get("SE1") is None or \
               st.session_state.get("SE2") is None or \
               st.session_state.get("SE3") is None or \
               st.session_state.get("SE4") is None or \
               st.session_state.get("SE5") is None or \
               st.session_state.get("SE6") is None or \
               st.session_state.get("SE7") is None or \
               st.session_state.get("SE8") is None or \
               st.session_state.get("SE9") is None or \
               st.session_state.get("SE10") is None:
                   warning_needed = True
            else:
                     st.session_state["end_time"] = datetime.now(tz)
                     row_data = [st.session_state["ID"],
                              st.session_state["ID"], st.session_state["gender"], st.session_state["age"],
                              st.session_state["self_esteem1"], st.session_state["self_esteem2"],
                              st.session_state["self_esteem3"], st.session_state["self_esteem4"],
                              st.session_state["self_esteem5"], st.session_state["self_esteem6"],
                              st.session_state["self_esteem7"], st.session_state["self_esteem8"],
                              st.session_state["self_esteem9"], st.session_state["self_esteem10"],
                              st.session_state["mindset1"], st.session_state["mindset2"], st.session_state["mindset3"],
                              st.session_state["important"], st.session_state["important"], st.session_state["important"], 
                              st.session_state["prac1"], st.session_state["prac2"],
                              st.session_state["score1"], st.session_state["score2"], st.session_state["comparison"],
                              st.session_state["ME1"], st.session_state["ME2"], st.session_state["ME3"],
                              st.session_state["SE1"], st.session_state["SE2"], st.session_state["SE3"],
                              st.session_state["SE4"], st.session_state["SE5"], st.session_state["SE6"], 
                              st.session_state["SE7"], st.session_state["SE8"], st.session_state["SE9"], st.session_state["SE10"],
                              st.session_state.get("end_time").strftime("%Y-%m-%d %H:%M:%S")
                     ]
                     sheet.append_row(row_data)
                     next_page()  # 跳到下一頁
                     st.rerun()
    if warning_needed: st.warning("⚠️ 請填寫所有問題才能繼續。")

# debrief
if st.session_state.page == 125:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("實驗目的澄清")
    st.markdown("---")
    st.write("""再次感謝您完成了本測驗！""")
    st.write("""我們的真實研究目的是想要了解受試者在練習時的努力狀況以及與他人的分數差異，會如何影響受試者對自己能力與表現的看法。""")
    st.write("""因此【正式測驗分數並不是真的】，請您別將分數作為判斷自己能力的依據！""")
    st.write("""最後，也請您勿將本研究與測驗內容告知任何人""")
    st.write("""如果您有任何疑問，請直接詢問研究人員。""")
    st.write("""敬祝平安健康順心！""")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])

    with col3:
        st.button("結束實驗", on_click=next_page)

#完成頁面
elif st.session_state.page == 126:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.success("實驗已完成！非常感謝您的參與。")
    st.balloons()
