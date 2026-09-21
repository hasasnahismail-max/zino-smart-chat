import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # Configure API key securely from Streamlit secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."

        # رد مباشر وفوري يضمن ذكر اسمك واسم التطبيق عند السؤال عن الهوية أو التأسيس
        prompt_lower = prompt.lower()
        if any(keyword in prompt_lower for keyword in ["مؤسس", "مطور", "صممك", "خالقك", "founder", "created", "developer", "built", "who are you"]):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # Try stable modern models with automatic fallback
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
            return "I am ZINO AI Chat, engineered and developed by Ismail Bassam (IBH). How can I help you today?"

        # Replace any accidental Google mentions
        response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
        response_text = response_text.replace("جوجل", "Ismail Bassam (IBH)")
        
        return response_text
        
    except Exception as e:
        return f"Error processing request: {str(e)}"
