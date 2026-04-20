import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

# 页面设置
st.set_page_config(page_title="MBTI Personality Test", layout="wide")
st.title("🧩 MBTI Personality Test")
st.subheader("Random Questions • Previous / Next • Radar Chart • Full Analysis")

# 初始化状态
if "stage" not in st.session_state:
    st.session_state.stage = "start"
if "answers" not in st.session_state:
    st.session_state.answers = []
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

# 题库
all_questions = [
    {"q": "You feel energized by social gatherings", "type": "E/I"},
    {"q": "You prefer small groups over large crowds", "type": "E/I"},
    {"q": "You often take the lead in conversations", "type": "E/I"},
    {"q": "You feel drained after long social events", "type": "E/I"},
    {"q": "You enjoy being the center of attention", "type": "E/I"},
    {"q": "You recharge by being alone", "type": "E/I"},
    {"q": "You focus on facts and details", "type": "N/S"},
    {"q": "You focus on ideas and possibilities", "type": "N/S"},
    {"q": "You trust your experiences more than imagination", "type": "N/S"},
    {"q": "You trust your intuition more than facts", "type": "N/S"},
    {"q": "You make decisions based on logic", "type": "T/F"},
    {"q": "You make decisions based on feelings", "type": "T/F"},
    {"q": "You value honesty over harmony", "type": "T/F"},
    {"q": "You value harmony over honesty", "type": "T/F"},
    {"q": "You prefer plans over spontaneity", "type": "J/P"},
    {"q": "You prefer spontaneity over plans", "type": "J/P"},
    {"q": "You like to finish tasks early", "type": "J/P"},
    {"q": "You work best under pressure", "type": "J/P"},
    {"q": "You listen more than you talk", "type": "E/I"},
    {"q": "You see the big picture easily", "type": "N/S"},
]

# 16型人格完整解读
full_descriptions = {
    "INTJ": "**The Architect** - Strategic, independent, visionary, logical.",
    "INTP": "**The Logician** - Inventive, curious, abstract, analytical.",
    "ENTJ": "**The Commander** - Bold, decisive, efficient, leader-like.",
    "ENTP": "**The Debater** - Smart, challenge-driven, creative, energetic.",
    "INFJ": "**The Advocate** - Idealistic, principled, caring, passionate.",
    "INFP": "**The Mediator** - Kind, creative, empathetic, loyal.",
    "ENFJ": "**The Protagonist** - Charismatic, inspiring, helpful.",
    "ENFP": "**The Campaigner** - Enthusiastic, social, creative, free-spirited.",
    "ISTJ": "**The Logistician** - Practical, reliable, responsible, factual.",
    "ISFJ": "**The Defender** - Dedicated, warm, protective, loyal.",
    "ESTJ": "**The Executive** - Efficient, traditional, strong administrator.",
    "ESFJ": "**The Consul** - Caring, social, popular, community-focused.",
    "ISTP": "**The Virtuoso** - Bold, practical, adaptable, tool-master.",
    "ISFP": "**The Adventurer** - Flexible, artistic, gentle, sensitive.",
    "ESTP": "**The Entrepreneur** - Energetic, perceptive, moment-living.",
    "ESFP": "**The Entertainer** - Spontaneous, fun, joyful, people-loving."
}

# 开始界面
if st.session_state.stage == "start":
    st.info("Click START to begin. You can go back and forth between questions.")
    if st.button("Start Test", type="primary"):
        st.session_state.selected_questions = random.sample(all_questions, 10)
        st.session_state.answers = [None] * 10
        st.session_state.current_q = 0
        st.session_state.stage = "test"
        st.rerun()

# 答题界面（带 上一题 / 下一题）
elif st.session_state.stage == "test":
    questions = st.session_state.selected_questions
    total = len(questions)
    idx = st.session_state.current_q

    st.progress((idx + 1) / total)
    st.write(f"### Question {idx + 1} / {total}")
    st.write(questions[idx]["q"])

    # 选项
    res = st.radio("Your choice:", ["Agree", "Disagree"], horizontal=True)
    st.session_state.answers[idx] = 1 if res == "Agree" else 0

    # 按钮
    col1, col2 = st.columns(2)
    with col1:
        if idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()
    with col2:
        if idx < total - 1:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("See Results →", type="primary", use_container_width=True):
                st.session_state.stage = "result"
                st.rerun()

# 结果界面
elif st.session_state.stage == "result":
    E = I = N = S = T = F = J = P = 0
    for ans, q in zip(st.session_state.answers, st.session_state.selected_questions):
        t = q["type"]
        if t == "E/I":
            E += ans
            I += 1 - ans
        elif t == "N/S":
            N += ans
            S += 1 - ans
        elif t == "T/F":
            T += ans
            F += 1 - ans
        elif t == "J/P":
            J += ans
            P += 1 - ans

    type_result = ("E" if E >= I else "I") + ("N" if N >= S else "S") + ("T" if T >= F else "F") + ("J" if J >= P else "P")

    st.success(f"# Your MBTI Type: {type_result}")
    st.write(full_descriptions[type_result])

    # 雷达图
    categories = ['Extraversion', 'Intuition', 'Thinking', 'Judging']
    values = [
        E/(E+I) if E+I else 0,
        N/(N+S) if N+S else 0,
        T/(T+F) if T+F else 0,
        J/(J+P) if J+P else 0
    ]
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color="#4285F4", alpha=0.3)
    ax.plot(angles, values, color="#4285F4", linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    st.pyplot(fig)

    if st.button("Start New Test"):
        st.session_state.stage = "start"
        st.rerun()