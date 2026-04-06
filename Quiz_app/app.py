import streamlit as st
import pandas as pd
import time

from questions import questions
from database import create_table, insert_result
from utils import calculate_score, get_feedback, get_result_summary

# -------------------------------
# 🔧 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Quiz App", page_icon="🧠", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #dbeafe, #fce7f3);
    color: #1f2937;
}

.block-container {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 15px;
}

h1 {
    font-size: 42px !important;
    color: #111827;
}

h3, .stMarkdown p {
    font-size: 20px !important;
    color: #111827 !important;
}

div[data-baseweb="radio"] {
    background-color: #ffffff;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 18px;
}

.stButton>button {
    background-color: #3b82f6;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🔧 INIT DB
# -------------------------------
create_table()

# -------------------------------
# 🧠 TITLE
# -------------------------------
st.title("🧠 Python Quiz App")
st.write("Test your knowledge and get instant feedback!")

# -------------------------------
# 👤 USER INPUT
# -------------------------------
name = st.text_input("Enter your name")
level = st.selectbox("Select Difficulty", ["Basic", "Intermediate", "Advanced"])

# -------------------------------
# 🚀 START QUIZ
# -------------------------------
# -------------------------------
# 🚀 START QUIZ (STEP-BY-STEP)
# -------------------------------
if name and level:

    st.subheader(f"🎯 All the Best {name}!")

    # ---------------------------
    # SESSION STATE INIT
    # ---------------------------
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state.start_time = time.time()

    total_q = len(questions[level])
    current_q = st.session_state.q_index

    # ---------------------------
    # QUIZ END
    # ---------------------------
    if current_q >= total_q:

        score = calculate_score(questions[level], st.session_state.answers)
        insert_result(name, score, total_q)

        st.success(f"🎉 Your Score: {score} / {total_q}")

        df = pd.DataFrame({
            "Question": [q["question"] for q in questions[level]],
            "Your Answer": st.session_state.answers,
            "Correct Answer": [q["answer"] for q in questions[level]]
        })

        st.dataframe(df)

        if st.button("Restart Quiz 🔄"):
            st.session_state.clear()
            st.rerun()

        st.stop()

    # ---------------------------
    # CURRENT QUESTION
    # ---------------------------
    q = questions[level][current_q]

    # ---------------------------
    # ⏱️ TIMER PER QUESTION
    # ---------------------------
    TOTAL_TIME = 10

    time_passed = int(time.time() - st.session_state.start_time)
    time_left = TOTAL_TIME - time_passed

    progress = time_left / TOTAL_TIME
    st.progress(max(progress, 0))

    if time_left <= 0:
        st.warning("⏰ Time's up! Moving to next question...")

        st.session_state.answers.append(None)
        st.session_state.q_index += 1
        st.session_state.start_time = time.time()
        st.rerun()

    if time_left <= 3:
        st.error(f"⚠️ {time_left}s left")
    else:
        st.info(f"⏳ Time Left: {time_left}s")

    # ---------------------------
    # 📌 QUESTION CARD UI
    # ---------------------------
    st.markdown(f"""
    <div style="
        background-color:#ffffff;
        padding:20px;
        border-radius:15px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);
        margin-bottom:20px;
    ">
        <h3>Question {current_q+1} of {total_q}</h3>
        <p style="font-size:20px;"><b>{q['question']}</b></p>
    </div>
    """, unsafe_allow_html=True)

    answer = st.radio(
        "Choose your answer:",
        q["options"],
        index=None,
        key=f"q_{current_q}"
    )

    # ---------------------------
    # NEXT BUTTON
    # ---------------------------
    if st.button("Next ➡️"):

        st.session_state.answers.append(answer)
        st.session_state.q_index += 1
        st.session_state.start_time = time.time()
        st.rerun()
