import os
import streamlit as st
import google.generativeai as genai

# Retrieve Gemini API key from Streamlit Secrets or Environment Variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

DEFAULT_MODEL = "gemini-1.5-flash"

def generate_response(prompt: str, system_instruction: str = None) -> str:
    """Generate a response using the Gemini AI model."""
    if not api_key:
        return "Error: GEMINI_API_KEY is not configured in Streamlit Secrets."
    try:
        model = genai.GenerativeModel(
            model_name=DEFAULT_MODEL,
            system_instruction=system_instruction
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while connecting to AI engine: {e}"

def summarize(text: str) -> str:
    """Summarize the provided text."""
    prompt = f"Please provide a concise and clear summary of the following text:\n\n{text}"
    return generate_response(prompt)

def summarize_text(text: str) -> str:
    """Alternative function for text summarization."""
    return summarize(text)

def summarize_chat(chat_history: list) -> str:
    """Summarize the chat history."""
    formatted_chat = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in chat_history])
    return summarize(formatted_chat)
