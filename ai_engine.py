import os
import google.generativeai as genai
from PIL import Image

API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

def deconstruct_engineering_page(image_file, language="English") -> str:
    """
    ZINO Vision Engine: Core deconstruction pipeline engineered by Ismail Hasasnah.
    """
    if not API_KEY:
        return "⚠️ API Key is missing. Please set GEMINI_API_KEY in Streamlit Secrets."

    try:
        img = Image.open(image_file)

        prompt = f"""
        You are ZINO Vision Engine using Feynman Methodology.
        Analyze and deconstruct this engineering or mathematical textbook image.

        Target Output Language: {language}

        Please structure your output strictly in Markdown as follows:
        ---
        ## 📐 1. Academic & Mathematical Rigor
        * **Core Formula / Theorem:** State formulas in clear LaTeX format ($E = mc^2$).
        * **Variable Definitions:** Symbols and their physical units.
        * **Engineering Context:** Step-by-step application breakdown.

        ---
        ## 💡 2. Feynman Intuitive Analogy
        * **The Analogy:** Simple everyday story explaining the concept clearly.
        * **Golden Rule:** One core takeaway sentence.
        ---
        """

        models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
        last_error = ""

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([prompt, img])
                return response.text
            except Exception as e:
                last_error = str(e)
                continue

        return f"⏳ **API Limit / Error:** {last_error}"

    except Exception as e:
        return f"⚠️ Processing Error: {str(e)}"
