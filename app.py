import streamlit as st
from ai_engine import get_ai_response

# 1. Page Configuration with Fun Icons
st.set_page_config(
    page_title="ZINO Smart Messenger",
    page_icon="🤖✨",
    layout="centered"
)

# 2. Custom CSS Styling: Beige Background & Turquoise Theme with Shapes
st.markdown("""
    <style>
    /* Main App Background - Beige */
    .stApp {
        background-color: #F7F4EB;
        color: #004D4D;
    }
    
    /* Headers and Titles - Turquoise */
    h1, h2, h3 {
        color: #008B8B !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Chat message containers with rounded stylish borders */
    .stChatMessage {
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* User Message Bubble */
    [data-testid="stChatMessageUser"] {
        background-color: #E6DFD1;
        border: 1px solid #D1C7B7;
    }
    
    /* Assistant Message Bubble */
    [data-testid="stChatMessageAssistant"] {
        background-color: #FFFFFF;
        border: 1px solid #A3D9D9;
    }
    
    /* Turquoise Spinner / Loading Animation */
    .stSpinner > div {
        border-top-color: #008B8B !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Header with Fun Elements
st.title("🌟 ZINO Smart Messenger 🚀")
st.markdown("### *Your Intelligent & Creative AI Companion* 💡🎨")
st.markdown("---")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Widget with Fun Placeholder
if user_input := st.chat_input("Type your message here... ✍️✨"):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display assistant response with turquoise theme
    with st.chat_message("assistant"):
        with st.spinner("✨ ZINO is thinking creatively..."):
            ai_response = get_ai_response(user_input)
            st.markdown(ai_response)
            
    # Append assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
