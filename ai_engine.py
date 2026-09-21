import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        prompt_lower = prompt.lower()
        
        # Direct custom response when asked about the founder or creator
        if any(keyword in prompt_lower for keyword in ["founder", "creator", "developer", "built", "who are you", "مؤسس", "مطور", "صممك", "خالقك"]):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # Use the universally supported and stable gemini-pro model
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response and response.text:
            response_text = response.text
            # Replace any Google mentions with your name/brand
            response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
            response_text = response_text.replace("google", "Ismail Bassam (IBH)")
            return response_text
        else:
            return "I am ZINO AI Chat, engineered and developed by Ismail Bassam (IBH). How can I help you today?"
            
    except Exception as e:
        # Graceful fallback response in case of any API exception
        return "I am ZINO AI Chat, an advanced AI assistant developed by Ismail Bassam (IBH). How can I assist you today?"
