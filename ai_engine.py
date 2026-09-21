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
        
        # Direct custom response only when asked about the founder or creator
        if any(keyword in prompt_lower for keyword in ["founder", "creator", "developer", "built", "who are you", "مؤسس", "مطور", "صممك", "خالقك"]):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # Use the highly stable and fast gemini-1.5-flash model for all other queries
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if response and response.text:
            response_text = response.text
            # Clean up any Google mentions and replace with your brand/name
            response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
            response_text = response_text.replace("google", "Ismail Bassam (IBH)")
            return response_text
        else:
            return "Error: Received an empty response from the model. Please try again."
            
    except Exception as e:
        return f"Error processing request: {str(e)}"
