import google.generativeai as genai
import streamlit as st

def get_ai_response(prompt: str) -> str:
    """
    Core AI Engine for ZINO AI Chat.
    Handles authentication, primary model routing, and automatic fallback.
    """
    try:
        # 1. Fetch API key securely from Streamlit Secrets
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: GEMINI_API_KEY is not configured in Streamlit Secrets."

        genai.configure(api_key=api_key)

        # 2. Sequential fallback candidates
        candidate_models = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-1.0-pro"
        ]

        # 3. Attempt execution with candidate models
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text') and response.text:
                    return response.text
            except Exception:
                continue

        # 4. Fallback: Dynamic API model discovery if named models fail
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    try:
                        model = genai.GenerativeModel(m.name)
                        response = model.generate_content(prompt)
                        if response and hasattr(response, 'text') and response.text:
                            return response.text
                    except Exception:
                        continue
        except Exception as discovery_err:
            return f"API Connection Error: {str(discovery_err)}"

        return "Error: Unable to connect to Gemini API models. Check API key permissions."

    except Exception as e:
        return f"System Runtime Error: {str(e)}"
