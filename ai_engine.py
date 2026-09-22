import os
import time
import google.generativeai as genai
from PIL import Image

# Configure Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

def deconstruct_engineering_page(image_file, language: str = "العربية") -> str:
    """
    ZINO Feynman Engine: Deconstructs complex STEM book pages into 
    rigorous LaTeX math and intuitive Feynman-style analogies.
    Supports Arabic, Russian, and English outputs.
    """
    model = genai.GenerativeModel("gemini-3.6-flash")
    img = Image.open(image_file)

    # Multi-language configuration prompt
    lang_instructions = {
        "العربية": "Write the complete analytical response in fluent, highly articulate ARABIC (اللغة العربية). Keep all mathematical formulas strictly in LaTeX standard format.",
        "Русский": "Write the complete analytical response in fluent, technical RUSSIAN (Русский язык). Keep all mathematical formulas strictly in LaTeX standard format.",
        "English": "Write the complete analytical response in precise ENGLISH. Keep all mathematical formulas strictly in LaTeX standard format."
    }

    selected_lang_instruction = lang_instructions.get(language, lang_instructions["العربية"])

    system_instruction = f"""
    You are the ZINO Feynman Vision Engine, an advanced AI system designed to deconstruct complex STEM, engineering, and pure mathematics textbook pages.
    Analyze the provided image of the textbook page and perform a Dual-Stream Deconstruction.

    TARGET LANGUAGE REQUIREMENT:
    {selected_lang_instruction}

    OUTPUT STRUCTURE (Use headers in the target language):
    ---
    ## 📐 1. Academic & Mathematical Rigor
    * **Core Formula / Theorem:** State the central mathematical or physical formulas explicitly using LaTeX format (e.g., $E = mc^2$ or $$\\int_{a}^{b} f(x) dx$$).
    * **Variable Definitions:** Clearly define each symbol, constant, and variable with its physical or mathematical units.
    * **Engineering Context & Derivation:** Provide a concise step-by-step breakdown of how this formula is applied in real-world engineering problems.

    ---
    ## 💡 2. Feynman Intuitive Analogy (For a 10-Year-Old)
    * **The Story / Real-World Analogy:** Explain this complex concept using a simple, relatable everyday story (e.g., flying a kite, water pipe flow, toy cars, swings) that a 10-year-old child can immediately visualize and understand.
    * **Golden Rule in One Sentence:** Summarize the core intuition behind this page in a single simple sentence.
    ---
    """

    prompt = f"Analyze and deconstruct this engineering/mathematics textbook page in {language} using the ZINO Feynman methodology."

    max_retries = 3
    retry_delay = 12

    for attempt in range(max_retries):
        try:
            response = model.generate_content([system_instruction, img, prompt])
            return response.text
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "Quota" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
            return f"⚠️ حدث ضغط مؤقت على السيرفر. يرجى إعادة المحاولة خلال ثوانٍ.\nالتفاصيل: {error_str}"
