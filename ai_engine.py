import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        # Use the stable and reliable gemini-pro model for normal operation
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "Error: Empty response received from the model."
            
    except Exception as e:
        return f"Error processing request: {str(e)}"
