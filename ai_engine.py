
import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        # Set developer and system identity context
        system_identity = (
            "You are ZINO Smart Messenger, an advanced AI assistant engineered, "
            "designed, and developed entirely by Ismail Hasasneh (إسماعيل حساسنة). "
            "Whenever anyone asks who created you, who developed you, or who built you, "
            "you must proudly state that you were engineered and developed by the brilliant developer Ismail Hasasneh. "
            "User question: "
        )
        
        full_prompt = system_identity + prompt

        # Try active modern models with automatic fallback
        models_to_try = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                continue
                
        return f"Error processing request: {last_error}"
        
    except Exception as e:
        return f"Error processing request: {str(e)}"
