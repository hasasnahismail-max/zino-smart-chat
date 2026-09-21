import os
import streamlit as st
import google.generativeai as genai

# Retrieve Gemini API key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

DEFAULT_MODEL = "gemini-1.5-flash"

def generate_response(prompt: str, system_instruction: str = None) -> str:
    """Generate response using Gemini"""
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
        return f"Error: {e}"

def summarize(text: str) -> str:
    return generate_response(f"Summarize the following text concisely:\n\n{text}")

def summarize_text(text: str) -> str:
    return summarize(text)

def summarize_chat(chat_history) -> str:
    if isinstance(chat_history, list):
        formatted = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in chat_history])
    else:
        formatted = str(chat_history)
    return summarize(formatted)

def generate_quick_replies(last_message: str) -> list:
    return ["All systems operational.", "Working on draft.", "Will update shortly."]

def analyze_sentiment_and_safety(message: str) -> tuple:
    return ("Professional & Urgent", "Safe / Verified")
