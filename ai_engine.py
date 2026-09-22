import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

def deconstruct_engineering_page(image_file) -> str:
    """
    ZINO Feynman Engine: Deconstructs complex STEM book pages into 
    rigorous LaTeX math and intuitive Feynman-style analogies.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        img = Image.open(image_file)

        system_instruction = """
        You are the ZINO Feynman Vision Engine, an advanced AI system designed to deconstruct complex STEM, engineering, and pure mathematics textbook pages.
        Analyze the provided image of the textbook page and perform a Dual-Stream Deconstruction:

        ---
        ## 📐 1. Academic & Mathematical Rigor
        * **Core Formula / Theorem:** State the central mathematical or physical formulas explicitly using LaTeX format (e.g., $E = mc^2$ or $$\\int_{a}^{b} f(x) dx$$).
        * **Variable Definitions:** Clearly define each symbol, constant, and variable with its physical or mathematical units.
        * **Engineering Context & Derivation:** Provide a concise step-by-step breakdown of how this formula is applied in real-world engineering problems.

        ---
        ## 💡 2. Feynman Intuitive Analogy (For a 10-Year-Old)
        * **The Story / Real-World Analogy:** Explain this complex concept using a simple, relatable everyday story (e.g., water pipe flow, toy cars, swings, or playground physics) that a 10-year-old child can immediately visualize and understand.
        * **Golden Rule in One Sentence:** Summarize the core intuition behind this page in a single simple sentence.
        ---
        """

        prompt = "Analyze and deconstruct this engineering/mathematics textbook page according to the ZINO Feynman methodology."
        
        response = model.generate_content([system_instruction, img, prompt])
        return response.text

    except Exception as e:
        return f"❌ Error analyzing the page: {str(e)}"
