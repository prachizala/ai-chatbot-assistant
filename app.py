"""MentorAI - Intelligent Academic & Software Engineering Chatbot.

Built with Python, Streamlit, and conversational prompt architectures.
Supports multi-turn memory pruning, persona customization, and dual live/offline execution.
"""

import os
import streamlit as st

from chatbot_engine import (
    PERSONAS,
    ConversationManager,
    query_llm,
    estimate_tokens
)

st.set_page_config(
    page_title="MentorAI: Academic & Code Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #2563EB; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 MentorAI: Academic & Coding Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Conversational AI Tutor with Sliding-Window Memory & Dual Mode Execution | Built by Prachi Zala</div>', unsafe_allow_html=True)

# Initialize Session State
if "conversation_manager" not in st.session_state:
    st.session_state["conversation_manager"] = ConversationManager(persona_key="coding_mentor")

cm: ConversationManager = st.session_state["conversation_manager"]

# Sidebar Settings
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/bot.png", width=110)
    st.subheader("⚙️ Assistant Persona")

    persona_choices = {
        "coding_mentor": "💻 Coding & Software Mentor",
        "academic_tutor": "📚 Academic & Data Science Tutor",
        "quick_summarizer": "⚡ Concise Technical Summarizer"
    }
    selected_persona = st.selectbox(
        "Choose Persona:",
        options=list(persona_choices.keys()),
        format_func=lambda k: persona_choices[k],
        index=list(persona_choices.keys()).index(cm.persona_key)
    )

    if selected_persona != cm.persona_key:
        cm.change_persona(selected_persona)
        st.toast(f"Switched persona to {persona_choices[selected_persona]}")

    st.markdown("---")
    st.subheader("🔑 Connectivity Mode")
    api_mode = st.radio("Execution Backend:", ["Local Offline Engine", "Live Cloud API"], index=0)

    api_key = None
    if api_mode == "Live Cloud API":
        api_key = st.text_input("Enter LLM API Key:", type="password", help="OpenAI-compatible or supported LLM provider API key.")
        if not api_key:
            st.info("No key entered. Requests will automatically use the high-quality local offline engine.")
    else:
        st.success("Running in offline mode. Zero external API calls required.")

    st.markdown("---")
    st.metric("Estimated Memory Tokens", f"{cm.total_tokens()} / {cm.max_history_tokens}")
    token_ratio = min(1.0, max(0.0, float(cm.total_tokens() / cm.max_history_tokens)))
    st.progress(token_ratio)
    st.caption(f"Context Budget Utilization: {token_ratio * 100:.1f}%")

    c_clear, c_export = st.columns(2)
    with c_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            cm.clear()
            st.rerun()

    with c_export:
        md_transcript = cm.export_as_markdown()
        st.download_button(
            "📥 Export MD",
            data=md_transcript,
            file_name="chat_transcript.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 👩‍💻 Developer")
    st.markdown("**Prachi Zala**  \nBCA Student, Ahmedabad  \n[GitHub Profile](https://github.com/prachizala)")

# Display Chat History
display_messages = cm.get_display_messages()

if not display_messages:
    welcome_text = PERSONAS[cm.persona_key]["welcome"]
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(welcome_text)
        st.markdown("\n**Try asking:**\n- *\"How does binary search work in Python?\"*\n- *\"Explain recursion with a base case example.\"*\n- *\"Show me essential Pandas data cleaning idioms.\"*")

for msg in display_messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat Input
user_query = st.chat_input("Ask a question about Python, algorithms, data science, or coursework...")

if user_query:
    # 1. Add user message
    cm.add_message("user", user_query)

    # 2. Render user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # 3. Generate and render response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Generating response..."):
            response = query_llm(cm.messages, api_key=api_key)
            st.markdown(response)

    # 4. Save response in conversation state
    cm.add_message("assistant", response)
    st.rerun()
