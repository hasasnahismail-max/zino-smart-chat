import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # 1. التحقق من مفتاح الـ API
        if "GEMINI_API_KEY" not in st.secrets:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        # 2. جلب قائمة النماذج المتاحة لمفتاحك تلقائياً لتفادي خطأ 404
        selected_model = None
        try:
            available_models = [
                m.name for m in genai.list_models() 
                if 'generateContent' in m.supported_generation_methods
            ]
            
            # اختيار أفضل نموذج متاح من القائمة المسترجعة
            for model_name in available_models:
                if 'flash' in model_name or 'pro' in model_name:
                    selected_model = model_name
                    break
                    
            if not selected_model and available_models:
                selected_model = available_models[0]
        except Exception:
            # اسم احتياطي مع البادئة الرسمية
            selected_model = 'models/gemini-1.5-flash-latest'

        # 3. إنشاء واستدعاء النموذج المكتشف
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "Error: Empty response received from the model."
            
    except Exception as e:
        return f"Error processing request: {str(e)}"
