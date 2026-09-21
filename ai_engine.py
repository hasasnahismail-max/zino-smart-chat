import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt):
    try:
        # 1. Verify API Key
        if "GEMINI_API_KEY" not in st.secrets:
            return "Error: GEMINI_API_KEY is missing in Streamlit Secrets."
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        # 2. Dynamically fetch available models to guarantee 0% 404 errors
        working_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    working_models.append(m.name)
        except Exception:
            pass

        # Fallback list if model discovery is restricted
        if not working_models:
            working_models = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']

        # 3. Generate content using the first working model
        last_error = ""
        for model_name in working_models:
            if 'gemini' not in model_name.lower():
                continue
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                continue

        return f"Connection Error: {last_error}"

    except Exception as e:
        return f"System Error: {str(e)}"
