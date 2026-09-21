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
        
        # Custom direct response if the query is about the founder or creator
        if any(keyword in prompt_lower for keyword in ["founder", "creator", "developer", "built", "who are you", "مؤسس", "مطور", "صممك", "خالقك"]):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # For normal queries, let the model generate a response normally
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
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

        # Clean up any accidental Google mentions and replace with the founder's name
        response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
        response_text = response_text.replace("google", "Ismail Bassam (IBH)")
        
        return response_text
        
    except Exception as e:
        return f"Error processing request: {str(e)}"
