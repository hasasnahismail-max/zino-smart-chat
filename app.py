import streamlit as st

# Page configuration with logo icon
st.set_page_config(
    page_title="ZINO AI Chat",
    page_icon="1790031715637.png",
    layout="centered"
)

# Display logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1790031715637.png", width=140)

st.title("ZINO AI")
st.caption("AI Assistant for Intelligent Systems")

# Chat history management
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to ZINO AI! How can I assist you today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input and assistant response
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = f"Received your message: '{prompt}'. Model integration in progress."
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
