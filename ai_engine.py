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
        
        # 1. إجابة مخصصة فقط عند السؤال المباشر عن المؤسس أو المطور
        founder_keywords = ["founder", "creator", "developer", "built", "who are you", "مؤسس", "مطور", "صممك", "خالقك"]
        if any(kw in prompt_lower for kw in founder_keywords):
            return "I am ZINO AI Chat, an advanced AI assistant engineered, designed, and developed entirely by Ismail Bassam (IBH)."

        # 2. تجربة النماذج المتاحة بالتتابع لتجنب أخطاء 404 أو توقف الاتصال
        models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']
        
        response_text = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    response_text = response.text
                    break
            except Exception:
                continue
                
        if not response_text:
            return "عذراً، لم أتمكن من جلب الإجابة حالياً. يرجى المحاولة مرة أخرى."

        # 3. تنظيف أي ذكر لجوجل واستبداله باسمك الكريم
        response_text = response_text.replace("Google", "Ismail Bassam (IBH)")
        response_text = response_text.replace("google", "Ismail Bassam (IBH)")
        
        return response_text
        
    except Exception as e:
        return f"Error processing request: {str(e)}"
