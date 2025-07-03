import streamlit as st
import pandas as pd
import os
import time
from PIL import Image

# 插入 CSS 樣式來修改整體字體、間距、置中等
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

# /* 整個畫面寬度置中顯示 */
# main .block-container {
#     max-width: 800px;
#     margin: auto;
# }

/* 增加輸入欄位的字體大小 */
input, textarea {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

#計時器
# ✅ 初始化狀態
if 'page' not in st.session_state:
    st.session_state.page = 0  # 頁面 0 為歡迎頁
if 'start_time' not in st.session_state:
    st.session_state.start_time = None  # 尚未開始計時

# ✅ 設定換頁函式
def next_page():
    st.session_state.page += 1
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()  # ⏱️ 按下開始時才設定

# ✅ 顯示計時器（轉換為分＋秒格式）
if st.session_state.start_time:
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

# ✅ 歡迎頁（page == 0）
if st.session_state.page == 0:
    st.title("📝 歡迎參加測驗")
    st.write("本測驗包含數題圖片與選項，請專心作答。")
    st.button("👉 開始測驗", on_click=next_page)

# 初始化頁數狀態
if 'page' not in st.session_state:
    st.session_state.page = 1

# 定義換頁函式
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# 顯示內容根據頁數改變
if st.session_state.page == 1:
    st.header("基本資料")
    st.subheader("基本資料")
    st.write("請填寫以下問卷，完成後按提交。")
    st.title("題組 1")
    st.write("這是第一組題目")
    # 受試者基本資料
    age = st.number_input("請輸入您的年齡", min_value=10, max_value=100, step=1)
    gender = st.radio("請選擇您的性別", ["男", "女", "其他"])
    st.markdown('<div class="question-text">問題 1：你喜歡貓還是狗？</div>', unsafe_allow_html=True)
    st.radio("", ["貓", "狗"], key="q1")
    st.radio("問題 2：你喜歡早上還是晚上？", ["早上", "晚上"], key="q1_2")
    #插入圖片
    image1 = Image.open("螢幕擷取畫面 2025-07-03 115532.png")
    st.image(image1, caption="題目1")
    st.button("下一頁", on_click=next_page)
    
elif st.session_state.page == 2:
    st.title("題組 2")
    st.write("這是第二組題目")
    st.radio("問題 1：你喜歡咖啡還是茶？", ["咖啡", "茶"], key="q2_1")
    st.radio("問題 2：你喜歡夏天還是冬天？", ["夏天", "冬天"], key="q2_2")
    # st.button("上一頁", on_click=prev_page)
    from PIL import Image, ImageDraw
    def create_simple_shape(color, shape, size=(150,150)):
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)
    if shape == "circle":
        draw.ellipse([30,30,120,120], fill=color)
    elif shape == "square":
        draw.rectangle([30,30,120,120], fill=color)
    elif shape == "triangle":
        draw.polygon([(75,30),(30,120),(120,120)], fill=color)
    return img

    # 題目圖 (8格 - 3x3, 中間空白)
    context_imgs = []
    colors = ["red", "green", "blue", "red", "green", "blue", "red", "green"]
    shapes = ["circle", "circle", "circle", "square", "square", "square", "triangle", "triangle"]
    
    for i in range(8):
        img = create_simple_shape(colors[i], shapes[i])
        img.save(f"q001_context_{i}.png")
    
    # 選項圖 (8個選項，只有一個正確填中間空白格)
    choices_imgs = []
    choice_colors = ["red", "green", "blue", "red", "green", "blue", "red", "blue"]
    choice_shapes = ["circle", "circle", "circle", "square", "square", "square", "triangle", "triangle"]
    
    for i in range(8):
        img = create_simple_shape(choice_colors[i], choice_shapes[i])
        img.save(f"q001_choice_{i}.png")

    # 正確選項是 index 2（藍色圓形）
    correct_answer = 2

    st.button("下一頁", on_click=next_page)

elif st.session_state.page == 3:
    st.title("題組 3")
    st.write("這是第三組題目")
    st.radio("問題 1：請選擇您覺得正確的選項？", ["1", "2"], key="q3_1")
    st.radio("問題 2：請選擇您覺得正確的選項？", ["1", "2"], key="q3_2")
    st.button("提交", on_click=next_page)

elif st.session_state.page == 4:
    st.success("問卷已完成！非常感謝您的作答")


# st.write("---")
# st.header("測驗題目 (Likert 量表)")
# st.write("請依據您的看法，1 = 非常不同意，5 = 非常同意")

# q1 = st.slider("1️⃣ 我喜歡學習新知識。", 1, 5, 3)
# q2 = st.slider("2️⃣ 我能持續專注於任務上。", 1, 5, 3)
# q3 = st.slider("3️⃣ 遇到困難時我不容易放棄。", 1, 5, 3)
# q4 = st.slider("4️⃣ 我覺得自己能完成目標。", 1, 5, 3)
# q5 = st.slider("5️⃣ 我享受挑戰性的任務。", 1, 5, 3)

# if st.button("✅ 提交"):
#     if participant_id == "":
#         st.warning("請先輸入您的 ID 再提交。")
#     else:
#         result = pd.DataFrame({
#             "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "Participant_ID": [participant_id],
#             "Age": [age],
#             "Gender": [gender],
#             "Q1": [q1],
#             "Q2": [q2],
#             "Q3": [q3],
#             "Q4": [q4],
#             "Q5": [q5]
#         })

        # # 將結果儲存到 CSV
        # if os.path.exists("results.csv"):
        #     result.to_csv("results.csv", mode="a", header=False, index=False, encoding='utf-8-sig')
        # else:
        #     result.to_csv("results.csv", mode="w", header=True, index=False, encoding='utf-8-sig')

        # st.success(f"感謝您的填寫，{participant_id}！已成功提交測驗。")
        # st.balloons()
