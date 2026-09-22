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
    Supports Arabic, Russian, and English analytical outputs.
    """
    try:
        model = genai.GenerativeModel("gemini-3.6-flash")
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
        * **Core Formula / Theorem:** State central formulas explicitly using LaTeX ($E = mc^2$ or $$\\int_{{a}}^{{b}} f(x) dx$$).
        * **Variable Definitions:** Clearly define symbols and their physical/mathematical units.
        * **Engineering Context:** Provide a step-by-step breakdown of real-world application.

        ---
        ## 💡 2. Feynman Intuitive Analogy (For a 10-Year-Old)
        * **The Story / Analogy:** Explain using a clear, relatable everyday story that a child can visualize.
        * **Golden Rule in One Sentence:** Single core takeaway sentence.
        ---
        """

        prompt = f"Analyze and deconstruct this engineering page in {language}."

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content([system_instruction, img, prompt])
                return response.text
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                raise e

    except Exception as e:
        return f"⚠️ Exception occurred: {str(e)}"
