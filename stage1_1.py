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
    return client.open("experiment_data").worksheet("stage1-1")

sheet = get_sheet()

#初始化資料庫
for key in ["ID", "gender", "age",
            "self_esteem1", "self_esteem2", "self_esteem3", "self_esteem4", "self_esteem5"
           , "self_esteem6", "self_esteem7", "self_esteem8", "self_esteem9", "self_esteem10"
           , "mindset1", "mindset2", "mindset3", "important1", "important2", "important3"
           , "Num", "Time", "E1", "E2", "E3", "score1", "score2", "comparison", "SE1", "SE2", "SE3", "SE4", "SE5", "SE6", "SE7" 
           , "q_1", "q_2", "q_3", "q_4", "q_5", "q_6", "q_7", "q_8", "q_9", "q_10", "q_11", "q_12", "q_13", "q_14", "q_15"
           , "q_16", "q_17", "q_18", "q_19", "q_20", "q_21", "q_22", "q_23", "q_24", "q_25", "q_26", "q_27", "q_28", "q_29", "q_30"]:
    if key not in st.session_state:
        st.session_state[key] = None

# 預先設定：受試者編號 -> [允許開始時間, 允許結束時間]
participants = {
    "test00": [datetime(2025, 9, 13, 20, 30, 0, tzinfo=tz), datetime(2026, 9, 15, 21, 30, 0, tzinfo=tz)],
    "GsvY11": [datetime(2025, 9, 13, 20, 30, 0, tzinfo=tz), datetime(2025, 9, 15, 21, 30, 0, tzinfo=tz)],
    "CQNp11": [datetime(2025, 9, 16, 10, 0, 0, tzinfo=tz), datetime(2025, 9, 16, 11, 0, 0, tzinfo=tz)],
    "EqLD11": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2025, 9, 16, 14, 30, 0, tzinfo=tz)],
    "NcXB11": [datetime(2025, 9, 15, 14, 0, 0, tzinfo=tz), datetime(2025, 9, 15, 15, 0, 0, tzinfo=tz)],
    "UwgD11": [datetime(2025, 9, 16, 10, 0, 0, tzinfo=tz), datetime(2025, 9, 16, 11, 0, 0, tzinfo=tz)],
    "aUKf11": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2025, 9, 16, 14, 30, 0, tzinfo=tz)],
    "bmHW11": [datetime(2025, 9, 15, 14, 0, 0, tzinfo=tz), datetime(2025, 9, 15, 15, 0, 0, tzinfo=tz)],
    "nxZS11": [datetime(2025, 9, 16, 10, 0, 0, tzinfo=tz), datetime(2025, 9, 16, 11, 0, 0, tzinfo=tz)],
    "snTq11": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2025, 9, 16, 14, 30, 0, tzinfo=tz)],
    "vGTh11": [datetime(2025, 9, 16, 13, 30, 0, tzinfo=tz), datetime(2025, 9, 16, 14, 30, 0, tzinfo=tz)],
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
    st.markdown(f"⏱️ **練習時間：{minutes:02d} 分 {seconds:02d} 秒**")

# 歡迎頁
if st.session_state.page == 0:
    st.header("歡迎參加本測驗")
    st.markdown("---")
    st.write("""您好！首先非常感謝您願意參與本測驗，本測驗為政治大學心理學研究所進行的碩士學位研究。""")
    st.write("""研究目的是想要了解受試者在做智力測驗前的練習與正式測驗分數有何關聯。""")
    st.write(""" 本測驗採用現有且已被證實有效的智力測驗作為測驗材料，共分為兩階段：練習階段與正式測驗階段。""")
    st.write(""" 當您開始進行本測驗，將會透過受試者編號與實驗主機連線。""")
    st.write("""測驗完畢者可參加抽獎，獎項為XXX（研究者會從後台對照受試者編號並將獎品寄到填寫表單之電子郵件）""")
    st.write(""" 若您是需要換取課堂學分則需要參與現場實驗，且無法參加抽獎活動，謝謝！""")
    st.write("""您有完全自主性，可以自由決定是否參與以及繼續本測驗，若您感到不適，可以隨時中止測驗。""")
    st.write("""本研究不會對您造成任何風險，您所填寫的資料將完全保密。資料收回後將由研究人員電子歸檔與保存並進行統計數據分析，預計保留5年後全數刪除，請您放心。""")
    st.write("""當您按下【開始測驗】表示您同意上述內容。""")
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
    st.write("以下問題是想了解您的基本資訊，以及您的一些價值觀，填寫完畢後請按【下一頁】進入練習階段。")
    st.markdown("---")
    st.radio("請選擇您的生理性別", ["男", "女", "其他"], horizontal=True, index=None, key="gender")
    st.selectbox("請選擇您的年齡區間", ["18歲以下", "19-25歲", "26-35歲", "36-45歲", "46-55歲", "56-65歲", "65歲以上"], index=None, placeholder="請選擇", key="age")
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
    st.write("14. 對您來說，邏輯推理能力有多重要？")
    st.radio("（１=非常不重要，６=非常重要）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="important1")
    st.write("15. 對您來說，分析思考能力有多重要？")
    st.radio("（１=非常不重要，６=非常重要）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="important2")
    st.write("16. 對您來說，圖形理解能力有多重要？")
    st.radio("（１=非常不重要，６=非常重要）", ["1", "2", "3", "4", "5", "6"], horizontal=True, index=None, key="important3")

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
                          or st.session_state.get("mindset1") is None or st.session_state.get("mindset2") is None or st.session_state.get("mindset3") is None 
                          or st.session_state.get("important1") is None or st.session_state.get("important2") is None or st.session_state.get("important3") is None):
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
                                        st.session_state["important1"], st.session_state["important2"], st.session_state["important3"],
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
    st.write("""本階段設有100道智力測驗練習題，每道練習題都可以觀看解答。""")
    st.write("""練習階段將會計時，也請您記住自己最後共練習了幾題。""")
    st.write("""【請您至少練習5題】之後您可自行決定是否要繼續練習或直接進入正式測驗。""")              
    st.write("""了解以上敘述後，請按【開始練習】進入練習測驗""")
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
    
    # with col4:
    #     if st.button("直接進入正式測驗"):
    #         st.session_state.start_time = None
    #         st.session_state.page = 104
    #         st.session_state.scroll_to_top = True
    #         st.rerun()
    
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
    answer_value="1"
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

    for i in range(5):  # 顯示7秒（1秒更新一次）
        time.sleep(1)
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
            time_str1 = f"{minutes} 分 {seconds} 秒"
            st.metric(label="您在練習所花費的時間", value=time_str1)
            row_data = [st.session_state["ID"],                                        
                        st.session_state["ID"], st.session_state["gender"], st.session_state["age"],                                        
                        st.session_state["self_esteem1"], st.session_state["self_esteem2"],                                        
                        st.session_state["self_esteem3"], st.session_state["self_esteem4"],                                        
                        st.session_state["self_esteem5"], st.session_state["self_esteem6"],                                        
                        st.session_state["self_esteem7"], st.session_state["self_esteem8"],                                    
                        st.session_state["self_esteem9"], st.session_state["self_esteem10"],                                    
                        st.session_state["mindset1"], st.session_state["mindset2"], st.session_state["mindset3"],                                        
                        st.session_state["important1"], st.session_state["important2"], st.session_state["important3"],
                        time_str1
                       ]
            sheet.append_row(row_data)
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
    
    st.header("進入正式測驗前")
    st.markdown("---")
    st.write("""以下問題是想了解您的練習狀況。填寫完畢後請按【下一頁】進入正式測驗。""")
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
        st.text_input("請問您總共練習了多少題？", placeholder="請輸入數字",  key="Num")
        st.text_input("請問您總共練習了幾分鐘？", placeholder="請輸入數字",  key="Time")
        st.write("１. 您有多認真做剛才的練習題？")
        st.radio(
                 label="（１=非常不認真，６=非常認真）",
                 options=["1", "2", "3", "4", "5", "6"],
                 key="E1", horizontal=True, index=None
        )

        st.write("２. 您有多投入於練習階段？")
        st.radio(
                 label="（１=非常不投入，６=非常投入）",
                 options=["1", "2", "3", "4", "5", "6"],
                 key="E2", horizontal=True, index=None
        )

        st.write("３. 您在做練習題時有多努力？")
        st.radio(
                 label="（１=非常不努力，６=非常努力）",
                 options=["1", "2", "3", "4", "5", "6"],
                 key="E3", horizontal=True, index=None
        )
    
    if 'warning_message' in st.session_state and st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    st.markdown("---")
    spacer1, btn_col = st.columns([5, 1])

    with btn_col:
        warning_needed = False
        if st.button("下一頁"):
            # 檢查是否有漏填
            if (st.session_state.get("Num") is None or 
                st.session_state.get("Time") is None or 
                st.session_state.get("E1") is None or 
                st.session_state.get("E2") is None or 
                st.session_state.get("E3") is None):
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
                              st.session_state["important1"], st.session_state["important2"], st.session_state["important3"],
                              st.session_state["important3"], st.session_state["Num"], st.session_state["Time"], 
                              st.session_state["E1"], st.session_state["E2"], st.session_state["E3"],
                     ]
                     sheet.append_row(row_data)
                     next_page() 
                     st.rerun()
    if warning_needed: st.warning("⚠️ 請填寫所有問題才能繼續。")
                
# 正式測驗說明
if st.session_state.page == 106:
    st.header("第二階段：正式測驗")
    st.markdown("---")
    st.write("""歡迎您來到正式測驗階段！本階段設有30道智力測驗題目。""")
    st.write("""當您作答完畢後，系統將會計算您的測驗分數（滿分為100）""")
    st.write("""正式測驗無法跳回上一頁，請您確定填答後再按【下一頁】""")
    st.write("""了解以上敘述後，請按【開始測驗】進入正式測驗""")
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
                st.image(image1, caption=f"正式題 {page_number-106}")
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
                st.image(image1, caption=f"正式題 {page_number-106}")
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
                st.image(image1, caption=f"正式題 {page_number-106}")
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


# 1
question(
    page_number=107,
    question_image_path="new_folder/高級圖形一 (5).png",
    option_image_path="new_folder/高級圖形一選項 (5).png",
    radio_key="q_1"
)
        
# 2
question(
    page_number=108,
    question_image_path="new_folder/高級圖形二 (11).png",
    option_image_path="new_folder/高級圖形二選項 (11).png",
    radio_key="q_2"
)

# 3
question(
    page_number=109,
    question_image_path="new_folder/高級圖形二 (15).png",
    option_image_path="new_folder/高級圖形二選項 (15).png",
    radio_key="q_3",
)

# 4
question1(
    page_number=110,
    question_image_path="new_folder/區分 (20).png",
    option_image_path="new_folder/區分選項 (20).png",
    radio_key="q_4"
)

# 5
question1(
    page_number=111,
    question_image_path="new_folder/區分 (5).png",
    option_image_path="new_folder/區分選項 (5).png",
    radio_key="q_5",
)

# 6
question1(
    page_number=112,
    question_image_path="new_folder/區分 (40).png",
    option_image_path="new_folder/區分選項 (40).png",
    radio_key="q_6",
)

# 7
question2(
    page_number=113,
    question_image_path="new_folder/推理思考 (5).png",
    option_image_path="new_folder/推理思考選項 (5).png",
    radio_key="q_7",
)

# 8
question2(
    page_number=114,
    question_image_path="new_folder/羅桑二氏 (50).png",
    option_image_path="new_folder/羅桑二氏選項 (50).png",
    radio_key="q_8",
)

# 9
question2(
    page_number=115,
    question_image_path="new_folder/羅桑二氏 (30).png",
    option_image_path="new_folder/羅桑二氏選項 (30).png",
    radio_key="q_9",
)

# 10
question2(
    page_number=116,
    question_image_path="new_folder/羅桑二氏 (55).png",
    option_image_path="new_folder/羅桑二氏選項 (55).png",
    radio_key="q_10",
)

# 11
question(
    page_number=117,
    question_image_path="new_folder/高級圖形二 (20).png",
    option_image_path="new_folder/高級圖形二選項 (20).png",
    radio_key="q_11"
)

# 12
question(
    page_number=118,
    question_image_path="new_folder/高級圖形二 (5).png",
    option_image_path="new_folder/高級圖形二選項 (5).png",
    radio_key="q_12",
)

# 13
question1(
    page_number=119,
    question_image_path="new_folder/區分 (25).png",
    option_image_path="new_folder/區分選項 (25).png",
    radio_key="q_13"
)

# 14
question1(
    page_number=120,
    question_image_path="new_folder/區分 (30).png",
    option_image_path="new_folder/區分選項 (30).png",
    radio_key="q_14",
)

# 15
question1(
    page_number=121,
    question_image_path="new_folder/區分 (35).png",
    option_image_path="new_folder/區分選項 (35).png",
    radio_key="q_15",
)

# 16
question2(
    page_number=122,
    question_image_path="new_folder/推理思考 (7).png",
    option_image_path="new_folder/推理思考選項 (7).png",
    radio_key="q_16",
)

# 17
question2(
    page_number=123,
    question_image_path="new_folder/推理思考 (20).png",
    option_image_path="new_folder/推理思考選項 (20).png",
    radio_key="q_17",
)

# 18
question2(
    page_number=124,
    question_image_path="new_folder/羅桑二氏 (44).png",
    option_image_path="new_folder/羅桑二氏選項 (44).png",
    radio_key="q_18",
)

# 19
question2(
    page_number=125,
    question_image_path="new_folder/羅桑二氏 (45).png",
    option_image_path="new_folder/羅桑二氏選項 (45).png",
    radio_key="q_19",
)

# 20
question2(
    page_number=126,
    question_image_path="new_folder/羅桑二氏 (10).png",
    option_image_path="new_folder/羅桑二氏選項 (10).png",
    radio_key="q_20",
)

# 21
question(
    page_number=127,
    question_image_path="new_folder/高級圖形二 (30).png",
    option_image_path="new_folder/高級圖形二選項 (30).png",
    radio_key="q_21"
)

# 22
question(
    page_number=128,
    question_image_path="new_folder/高級圖形二 (25).png",
    option_image_path="new_folder/高級圖形二選項 (25).png",
    radio_key="q_22",
)

# 23
question1(
    page_number=129,
    question_image_path="new_folder/區分 (15).png",
    option_image_path="new_folder/區分選項 (15).png",
    radio_key="q_23"
)

# 24
question1(
    page_number=130,
    question_image_path="new_folder/區分 (10).png",
    option_image_path="new_folder/區分選項 (10).png",
    radio_key="q_24",
)

# 25
question1(
    page_number=131,
    question_image_path="new_folder/區分 (26).png",
    option_image_path="new_folder/區分選項 (26).png",
    radio_key="q_25",
)

# 26
question2(
    page_number=132,
    question_image_path="new_folder/推理思考 (15).png",
    option_image_path="new_folder/推理思考選項 (15).png",
    radio_key="q_26",
)

# 27
question2(
    page_number=133,
    question_image_path="new_folder/推理思考 (10).png",
    option_image_path="new_folder/推理思考選項 (10).png",
    radio_key="q_27",
)

# 28
question2(
    page_number=134,
    question_image_path="new_folder/羅桑二氏 (40).png",
    option_image_path="new_folder/羅桑二氏選項 (40).png",
    radio_key="q_28",
)

# 29
question2(
    page_number=135,
    question_image_path="new_folder/羅桑二氏 (5).png",
    option_image_path="new_folder/羅桑二氏選項 (5).png",
    radio_key="q_29",
)

# 30
question2(
    page_number=136,
    question_image_path="new_folder/羅桑二氏 (60).png",
    option_image_path="new_folder/羅桑二氏選項 (60).png",
    radio_key="q_30",
)

if st.session_state.page == 137:
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
                <h4>⏳ 分數計算中，請稍候…</h4>
            </div>
        """, unsafe_allow_html=True)

        # 放置進度條（放在 Markdown 之後，就會靠近頂部）
        progress_bar = st.progress(0)

    for i in range(10):
        time.sleep(1)
        progress_bar.progress((i + 1) * 10)

    # 處理完跳轉下一頁
    st.session_state.page += 1
    st.session_state.scroll_to_top = True
    st.rerun()
    
if st.session_state.page == 138:
    st.success("測驗結果分析完成！")
    st.header("測驗結果")
    st.markdown("---")

    if st.session_state.get("formal_start_time"):
        elapsed_seconds = int(time.time() - st.session_state.formal_start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_str2 = f"{minutes} 分 {seconds} 秒"
        row_data = [st.session_state["ID"],
                    st.session_state["ID"], st.session_state["gender"], st.session_state["age"],
                    st.session_state["self_esteem1"], st.session_state["self_esteem2"],
                    st.session_state["self_esteem3"], st.session_state["self_esteem4"],
                    st.session_state["self_esteem5"], st.session_state["self_esteem6"],
                    st.session_state["self_esteem7"], st.session_state["self_esteem8"],
                    st.session_state["self_esteem9"], st.session_state["self_esteem10"],
                    st.session_state["mindset1"], st.session_state["mindset2"], st.session_state["mindset3"],
                    st.session_state["important1"], st.session_state["important2"], st.session_state["important3"],
                    st.session_state["important3"], st.session_state["Num"], st.session_state["Time"],                              
                    st.session_state["E1"], st.session_state["E2"], st.session_state["E3"], time_str2
                   ]
        sheet.append_row(row_data)
    else:
        time_str2 = "無法取得"

    personal_score = 65
    average_score = 80
    Img = Image.open("new_folder/圖片1.png")
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col1:
             st.metric(label="您先前練習的題數", value=sheet.acell("V4").value)  
    with col2:
             st.metric(label="您先前的練習時長", value=sheet.acell("U4").value)  
    
    col1, col2, col3 = st.columns([1, 1, 2]) 
    with col1:
             st.metric(label="您的分數", value=f"{personal_score}") 
             
    with col2:
             st.metric(label="同齡人平均分數", value=f"{average_score}") 
     
    with col3:
             st.image(Img)
             
    # col1, col2, col3 = st.columns([2, 1, 2]) 
    # with col1: 
    #     st.metric(label="您在測驗所花費的時間", value=time_str2)  

    
         
    # col1, col2, col3 = st.columns([2, 1, 2])
    # with col1:
    #     st.metric(label="您的智力測驗分數", value=f"{personal_score}")
    # with col3:
    #     st.metric(label="與您同齡的人的平均分數", value=f"{average_score}")
        
    st.markdown("---")
    # 下一頁按鈕
    col1, col2 = st.columns([5, 2])
    with col2:
        if st.button("下一頁"):
            st.session_state.page += 1
            st.session_state.scroll_to_top = True
            st.rerun()

# 操弄檢核
if st.session_state.page == 139:
    if st.session_state.get("scroll_to_top", False):
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
            st.session_state.scroll_to_top = False
    st.header("正式測驗結束前")
    st.markdown("---")
    st.write("""以下問題是想了解您的正式測驗狀況。填寫完畢後請按【下一頁】。""")
    score1 = st.text_input("您的正式測驗分數是幾分？", placeholder="請輸入數字",  key="score1")
    score2 = st.text_input("同齡人平均測驗分數是幾分？", placeholder="請輸入數字", key="score2")
    comparison = st.radio("您的正式測驗分數比同齡人平均測驗分數高還是低？", ["高", "低", "不知道"], index=None, key="comparison")
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
            if score1 is None or score2 is None or comparison is None:
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
                              st.session_state["important1"], st.session_state["important2"], st.session_state["important3"],
                              st.session_state["important3"], st.session_state["Num"], st.session_state["Time"], 
                              st.session_state["E1"], st.session_state["E2"], st.session_state["E3"], st.session_state["E3"],
                              st.session_state["score1"], st.session_state["score2"], st.session_state["comparison"],
                     ]
                     sheet.append_row(row_data)
                     st.session_state.warning_message = "" 
                     st.session_state.page += 1
                     st.rerun()

# 測驗後問卷
if st.session_state.page == 140:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("結束本測驗前")
    st.markdown("---")
    st.write("""以下問題是想了解您的一些想法。填寫完畢後請按【完成測驗】。""")

    st.write("１. 您認為自己的邏輯推理能力如何？")
    SE1 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE1", horizontal=True, index=None
    )
    
    st.write("２. 您認為自己的分析思考能力如何？")
    SE2 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE2", horizontal=True, index=None
    )

    st.write("３. 您認為自己的分析思考能力如何？")
    SE3 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE3", horizontal=True, index=None
    )
    
    st.write("４. 您認為自己的正式測驗表現如何？")
    SE2 = st.radio(
        label="（１=非常不滿意，６=非常滿意）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE4", horizontal=True, index=None
    )

    st.write("５. 您對自己的正式測驗表現有多滿意？")
    SE3 = st.radio(
        label="（１=非常不好，６=非常好）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE5", horizontal=True, index=None
    )
    
    st.write("６. 您是否同意本測驗能正確測量到您的能力？")
    SE3 = st.radio(
        label="（１=非常不同意，６=非常同意）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE6", horizontal=True, index=None
    )
    
    st.write("７. 您是否同意本測驗的內容是有效的？")
    SE3 = st.radio(
        label="（１=非常不同意，６=非常同意）",
        options=["1", "2", "3", "4", "5", "6"],
        key="SE7", horizontal=True, index=None
    )

    
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
               st.session_state.get("SE7") is None:
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
                              st.session_state["important1"], st.session_state["important2"], st.session_state["important3"],
                              st.session_state["important3"], st.session_state["Num"], st.session_state["Time"], 
                              st.session_state["E1"], st.session_state["E2"], st.session_state["E3"], st.session_state["E3"],
                              st.session_state["score1"], st.session_state["score2"], st.session_state["comparison"],
                              st.session_state["SE1"], st.session_state["SE2"], st.session_state["SE3"], st.session_state["SE4"], 
                              st.session_state["SE5"], st.session_state["SE6"], st.session_state["SE7"],
                              st.session_state.get("end_time").strftime("%Y-%m-%d %H:%M:%S")
                     ]
                     sheet.append_row(row_data)
                     next_page()  # 跳到下一頁
                     st.rerun()
    if warning_needed: st.warning("⚠️ 請填寫所有問題才能繼續。")


# --- 在你的程式碼中加入這個區塊 ---
# 假設這是最後一頁
if st.session_state.page == 200:
    st.header("問卷結束")
    st.write("感謝您完成本次測驗。")
    st.write("請點擊下方按鈕提交您的資料。")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("提交資料", type="primary", on_click=submit_data):
            st.rerun() # 點擊後重新執行頁面，以顯示 success/error 訊息

    # df = pd.DataFrame(sheet.get_all_records())
    # st.dataframe(df)

# debrief
if st.session_state.page == 141:
    if st.session_state.get("scroll_to_top", False):
        st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    st.header("實驗目的澄清")
    st.markdown("---")
    st.write("""再次感謝您完成了本測驗！""")
    st.write("""我們的真實研究目的是想要了解受試者在練習時的努力狀況以及與他人的分數差異，會如何影響受試者對自己能力與表現的看法。""")
    st.write("""因此【正式測驗分數並不是真的】，請您別將分數作為判斷自己智力的依據！""")
    st.write("""最後，也請您勿將本研究與測驗內容告知任何人""")
    st.write("""如果您有任何疑問，可以直接聯繫研究人員（112752003@g.nccu.edu.tw）""")
    st.write("""祝您能在本研究的抽獎活動中中獎！也敬祝平安健康順心！""")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])

    with col3:
        st.button("結束實驗", on_click=next_page)

#完成頁面
elif st.session_state.page == 142:
    st.markdown("""<script>window.scrollTo(0, 0);</script>""", unsafe_allow_html=True)
    st.success("實驗已完成！非常感謝您的參與。")
    st.balloons()

