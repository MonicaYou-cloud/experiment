import streamlit as st
import pandas as pd
import os
from datetime import datetime

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
