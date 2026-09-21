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
        founder_keywords = ["founder", "creator", "developer", "built", "who are you"]
        if any(kw in prompt_lower for kw in founder_keywords):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # 2. Try the latest supported models and capture any errors
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    response_text = response.text
                    response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
                    response_text = response_text.replace("google", "Ismail Bassam (IBH)")
                    return response_text
            except Exception as e:
                last_error = str(e)
                continue
                
        # If all models fail, return the exact debug error details
        return f"Debug Error Details: {last_error}"
        
    except Exception as e:
        return f"System Error: {str(e)}"
