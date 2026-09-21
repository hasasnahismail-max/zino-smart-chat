import streamlit as st
from ai_engine import get_ai_response

# 1. Page Configuration
st.set_page_config(
    page_title="ZINO Smart Messenger",
    page_icon="🤖✨",
    layout="centered"
)

# 2. Custom CSS Styling: Beige Background & Turquoise Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #F7F4EB;
        color: #004D4D;
    }
    
    h1, h2, h3 {
        color: #008B8B !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stChatMessage {
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stChatMessageUser"] {
        background-color: #E6DFD1;
        border: 1px solid #D1C7B7;
    }
    
    [data-testid="stChatMessageAssistant"] {
        background-color: #FFFFFF;
        border: 1px solid #A3D9D9;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🌟 ZINO Smart Messenger 🚀")
st.markdown("### *Your Intelligent & Creative AI Companion* 💡🎨")

# Signature Banner / Your Fingerprint on the App
st.markdown("""
    <div style="background-color: #E6DFD1; padding: 12px; border-radius: 12px; text-align: center; border: 2px solid #008B8B; margin: 15px 0;">
        <span style="color: #008B8B; font-weight: bold; font-size: 16px;">✨ Engineered & Founded by Ismail Hasasneh (إسماعيل حساسنة) ✨</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Widget
if user_input := st.chat_input("Type your message here... ✍️✨"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("✨ ZINO is thinking creatively..."):
            ai_response = get_ai_response(user_input)
            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
