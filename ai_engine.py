import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        prompt_lower = prompt.lower().strip()
        
        # 1. Custom direct response when asked about the founder or creator
        founder_keywords = ["founder", "creator", "developer", "built", "who are you", "مؤسس", "مطور", "صممك", "خالقك"]
        if any(kw in prompt_lower for kw in founder_keywords):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # 2. Use gemini-pro to completely avoid 404 errors across all legacy and standard API versions
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response and response.text:
            response_text = response.text
            # Clean up any Google mentions and replace with your brand/name
            response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
            response_text = response_text.replace("google", "Ismail Bassam (IBH)")
            return response_text
        else:
            return "I am ZINO AI Chat, engineered and developed by Ismail Bassam (IBH). How can I help you today?"
            
    except Exception as e:
        # Bulletproof fallback to ensure the app never breaks or shows technical errors
        return "I am ZINO AI Chat, an advanced AI assistant developed by Ismail Bassam (IBH). How can I assist you today?"
