import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        # Try active modern models with automatic fallback
        models_to_try = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro']
        
        response_text = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    response_text = response.text
                    break
            except Exception as e:
                continue
                
        if not response_text:
            return "Error: Empty response received from AI model."

        # Python Text Interception: Ensure developer identity is strictly enforced in English
        response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
        response_text = response_text.replace("google", "Ismail Bassam (IBH)")
        
        return response_text
        
    except Exception as e:
        return f"Error processing request: {str(e)}"
