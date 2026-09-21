import streamlit as st
from ai_engine import get_ai_response

st.set_page_config(
    page_title="ZINO Smart Messenger",
    page_icon="🤖",
    layout="centered"
)

st.title("💬 ZINO Smart Messenger v1.0")
st.markdown("Engineered & Founded by Ismail Hasasneh | Intelligent Messaging Platform")

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages from history when re-rendering
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input via Streamlit chat input widget
if user_input := st.chat_input("Type your message here..."):
    # Append user message to state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = get_ai_response(user_input)
            st.markdown(ai_response)
            
    # Append assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
