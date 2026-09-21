import streamlit as st
from ai_engine import get_ai_response

# 1. Page Configuration
st.set_page_config(
    page_title="ZINO AI Chat",
    page_icon="🤖",
    layout="centered"
)

# 2. Styling (Beige & Turquoise Theme + Custom Banner)
st.markdown("""
    <style>
    .stApp {
        background-color: #FDFBF7;
    }
    .main-header {
        text-align: center;
        color: #008080;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
    }
    .ibh-banner {
        background-color: #E6F2F2;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        color: #006666;
        font-weight: 600;
        margin-bottom: 25px;
        border: 1px solid #B2D8D8;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header & Branding
st.markdown("<h1 class='main-header'>ZINO AI Chat</h1>", unsafe_allow_html=True)
st.markdown("<div class='ibh-banner'>✨ Engineered & Developed by Ismail Bassam (IBH) ✨</div>", unsafe_allow_html=True)

# 4. Initialize Session History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Prompt Logic
if prompt := st.chat_input("Type your message here... ✍️✨"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing response..."):
            response = get_ai_response(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
