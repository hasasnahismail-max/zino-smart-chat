
import google.generativeai as genai
import os

# Configure Gemini API key (Ensure GEMINI_API_KEY is set in your environment secrets)
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_ai_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing request: {str(e)}"
