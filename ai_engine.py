import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        # Try the latest active modern models
        models_to_try = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                continue
                
        return f"Error processing request: {last_error}"
        
    except Exception as e:
        return f"Error processing request: {str(e)}"
