import os
import time
import google.generativeai as genai
from PIL import Image

API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

def deconstruct_engineering_page(image_file, language: str = "العربية") -> str:
    """
    ZINO Vision Engine: Core deconstruction pipeline engineered by Ismail Hasasnah.
    Includes smart fallback logic for API Rate Limits (429 errors).
    """
    try:
        img = Image.open(image_file)

        lang_instructions = {
            "العربية": "Write the response in fluent ARABIC. Keep all mathematical formulas strictly in LaTeX format.",
            "Русский": "Write the response in fluent RUSSIAN. Keep all mathematical formulas strictly in LaTeX format.",
            "English": "Write the response in precise ENGLISH. Keep all mathematical formulas strictly in LaTeX format."
        }

        selected_instruction = lang_instructions.get(language, lang_instructions["العربية"])

        system_instruction = f"""
        You are the ZINO Vision Engine (Feynman Methodology).
        {selected_instruction}

        Output Structure:
        ---
        ## 📐 1. Academic & Mathematical Rigor
        * **Core Formula / Theorem:** State central formulas explicitly using LaTeX ($E = mc^2$).
        * **Variable Definitions:** Clearly define symbols and their physical/mathematical units.
        * **Engineering Context:** Provide a step-by-step breakdown of real-world application.

        ---
        ## 💡 2. Feynman Intuitive Analogy (For a 10-Year-Old)
        * **The Story / Analogy:** Explain using a clear, relatable everyday story.
        * **Golden Rule in One Sentence:** Single core takeaway sentence.
        ---
        """

        prompt = f"Analyze and deconstruct this engineering page in {language}."

        # المحاولة عبر عدة نماذج لتفادي أي ضغط على نموذج معين
        models_to_try = ["gemini-3.6-flash", "gemini-1.5-flash", "gemini-2.5-flash"]

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([system_instruction, img, prompt])
                return response.text
            except Exception as model_err:
                err_text = str(model_err)
                if "429" in err_text or "Quota" in err_text:
                    continue  # الانتقال للنموذج التالي تلقائياً
                raise model_err

        return "⏳ **Temporary API Limit:** Reached free tier speed limit. Please wait 60 seconds and try again."

    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "Quota" in err_msg:
            return "⏳ **API Rate Limit Reached:** Please wait about 1 minute before clicking again."
        return f"⚠️ Exception occurred: {err_msg}"
