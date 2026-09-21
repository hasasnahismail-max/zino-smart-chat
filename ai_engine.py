import google.generativeai as genai
import os

def get_ai_response(prompt):
    # List of models to try automatically to guarantee compatibility with your API key and version
    models_to_try = ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash']
    
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
