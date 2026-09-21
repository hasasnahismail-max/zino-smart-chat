import streamlit as st
from ai_engine import summarize_chat, generate_quick_replies, analyze_sentiment_and_safety

# Page Configuration
st.set_page_config(page_title="ZINO Smart Messenger", page_icon="💬", layout="wide")

# Custom CSS for Mobile Responsive WhatsApp-style UI
st.markdown("""
<style>
    .stApp { background-color: #0b141a; color: #e9edef; }
    .header-box {
        background-color: #202c33;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-bottom: 2px solid #00a884;
    }
    .user-msg {
        background-color: #005c4b;
        padding: 10px 14px;
        border-radius: 10px;
        margin: 5px 0;
        width: fit-content;
        max-width: 80%;
        margin-left: auto;
    }
    .incoming-msg {
        background-color: #202c33;
        padding: 10px 14px;
        border-radius: 10px;
        margin: 5px 0;
        width: fit-content;
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# Application Header & Portfolio Branding
st.markdown("""
<div class="header-box">
    <h2 style="color: #00a884; margin: 0;">ZINO Smart Messenger v1.0</h2>
    <small style="color: #8696a0;">Engineered & Founded by Ismail Hasasneh | Intelligent Messaging Platform</small>
</div>
""", unsafe_allow_html=True)

# Initialize Session Chat State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"sender": "Anas", "text": "Hi Ismail, have you verified the computer vision pipeline and diagnostic engine?"},
        {"sender": "Ashraf", "text": "Yes, performance metrics are solid and accuracy is well within operational limits."},
        {"sender": "Anas", "text": "Great! Let's finalize the technical whitepaper before 5 PM."}
    ]

# Sidebar Control Panel
with st.sidebar:
    st.title("⚙️ ZINO AI Control Panel")
    st.info("Intelligent messaging simulation platform powered by Natural Language Processing and LLMs.")
    
    st.subheader("AI Diagnostics")
    if st.button("📊 Summarize Chat History"):
        chat_text = "\n".join([f"{m['sender']}: {m['text']}" for m in st.session_state.messages])
        with st.spinner("Generating summary via ZINO AI Engine..."):
            summary = summarize_chat(chat_text)
            st.session_state.summary_result = summary

    if st.button("🔍 Analyze Sentiment & Safety"):
        last_msg = st.session_state.messages[-1]["text"]
        sentiment, safety = analyze_sentiment_and_safety(last_msg)
        st.session_state.sentiment_info = f"Tone: {sentiment} | Safety Guard: {safety}"

# Display AI Summary Section
if "summary_result" in st.session_state:
    st.success("### 📝 ZINO AI Executive Summary")
    st.write(st.session_state.summary_result)
    st.divider()

if "sentiment_info" in st.session_state:
    st.warning(f"🛡️ Message Analysis: {st.session_state.sentiment_info}")

# Active Chat Room Window
st.subheader("💬 Active Chat Stream")

for msg in st.session_state.messages:
    if msg["sender"] == "Me":
        st.markdown(f'<div class="user-msg"><b>{msg["sender"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="incoming-msg"><b>{msg["sender"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)

st.divider()

# Quick Replies & Message Input Section
last_incoming = [m["text"] for m in st.session_state.messages if m["sender"] != "Me"][-1]

st.write("💡 **ZINO AI Suggested Quick Replies:**")
cols = st.columns(3)
quick_replies = generate_quick_replies(last_incoming)

for idx, col in enumerate(cols):
    if idx < len(quick_replies):
        if col.button(quick_replies[idx], key=f"btn_{idx}"):
            st.session_state.messages.append({"sender": "Me", "text": quick_replies[idx]})
            st.rerun()

# New Message Input Bar
new_msg = st.text_input("Type your message here...", key="user_input")
if st.button("Send Message 🚀"):
    if new_msg.strip():
        st.session_state.messages.append({"sender": "Me", "text": new_msg})
        st.rerun()
