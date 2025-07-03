import streamlit as st
import pandas as pd
import os
from datetime import datetime

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
    st.title("📘 題組 1")
    st.write("這是第一組題目")
    st.radio("問題 1：你喜歡貓還是狗？", ["貓", "狗"], key="q1_1")
    st.radio("問題 2：你喜歡早上還是晚上？", ["早上", "晚上"], key="q1_2")
    st.button("下一頁", on_click=next_page)

elif st.session_state.page == 2:
    st.title("📙 題組 2")
    st.write("這是第二組題目")
    st.radio("問題 3：你喜歡咖啡還是茶？", ["咖啡", "茶"], key="q2_1")
    st.radio("問題 4：你喜歡夏天還是冬天？", ["夏天", "冬天"], key="q2_2")
    st.button("上一頁", on_click=prev_page)
    st.button("提交", on_click=lambda: st.success("問卷已完成！感謝作答 🙏"))

st.title("🧪 心理學測驗示範")
st.write("請填寫以下問卷，完成後按提交。")

# 受試者基本資料
participant_id = st.text_input("請輸入您的 ID（或暱稱）")
age = st.number_input("請輸入您的年齡", min_value=10, max_value=100, step=1)
gender = st.radio("請選擇您的性別", ["男", "女", "其他"])

st.write("---")
st.header("測驗題目 (Likert 量表)")
st.write("請依據您的看法，1 = 非常不同意，5 = 非常同意")

q1 = st.slider("1️⃣ 我喜歡學習新知識。", 1, 5, 3)
q2 = st.slider("2️⃣ 我能持續專注於任務上。", 1, 5, 3)
q3 = st.slider("3️⃣ 遇到困難時我不容易放棄。", 1, 5, 3)
q4 = st.slider("4️⃣ 我覺得自己能完成目標。", 1, 5, 3)
q5 = st.slider("5️⃣ 我享受挑戰性的任務。", 1, 5, 3)

if st.button("✅ 提交"):
    if participant_id == "":
        st.warning("請先輸入您的 ID 再提交。")
    else:
        result = pd.DataFrame({
            "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Participant_ID": [participant_id],
            "Age": [age],
            "Gender": [gender],
            "Q1": [q1],
            "Q2": [q2],
            "Q3": [q3],
            "Q4": [q4],
            "Q5": [q5]
        })

        # 將結果儲存到 CSV
        if os.path.exists("results.csv"):
            result.to_csv("results.csv", mode="a", header=False, index=False, encoding='utf-8-sig')
        else:
            result.to_csv("results.csv", mode="w", header=True, index=False, encoding='utf-8-sig')

        st.success(f"感謝您的填寫，{participant_id}！已成功提交測驗。")
        st.balloons()
