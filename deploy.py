import streamlit as st
from trail_4 import chat

st.set_page_config(
    page_title="CALM — Calculus Tutor",
    page_icon="📐",
    layout="centered"
)

st.title("📐 CALM — Adaptive Calculus Tutor")
st.caption("Based on Thomas' Calculus | Powered by BKT + LLM")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "student_concept" not in st.session_state:
    st.session_state.student_concept = {
        "P_mastery": 0.10,
        "P_guess":   0.10,
        "P_slip":    0.10
    }

if "data_student" not in st.session_state:
    st.session_state.data_student = {
        "following_action": "",
        "user_prompt":      "",
        "llm_response":     "",
        "current_chapter":  ""
    }

mastery = st.session_state.student_concept["P_mastery"]

col1, col2 = st.columns([3, 1])
with col1:
    st.progress(mastery, text=f"Mastery Level: {mastery:.0%}")
with col2:
    if mastery < 0.40:
        st.markdown("🟥 Beginner")
    elif mastery < 0.70:
        st.markdown("🟨 Developing")
    else:
        st.markdown("🟩 Proficient")

st.divider()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question or answer the tutor...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text, updated_concept, updated_data, control = chat(
                user_input          = user_input,
                chat_history        = st.session_state.chat_history,
                student_concept     = st.session_state.student_concept,
                data_student        = st.session_state.data_student
            )
        st.markdown(response_text)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response_text
    })
    st.session_state.student_concept = updated_concept
    st.session_state.data_student    = updated_data

    st.rerun()
