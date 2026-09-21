import streamlit as st
from ai_engine import get_ai_response

# Page Configuration
st.set_page_config(
    page_title="ZINO AI Chat",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for Beige and Turquoise Theme & IBH Signature Banner
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
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: #006666;
        font-weight: 600;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header & IBH Signature Banner
st.markdown("<h1 class='main-header'>ZINO AI Chat</h1>", unsafe_allow_html=True)
st.markdown("<div class='ibh-banner'>✨ Engineered & Developed by Ismail Bassam (IBH) ✨</div>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here... ✍️✨"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
