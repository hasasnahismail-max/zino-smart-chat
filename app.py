import os
import streamlit as st
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="ZINO Vision Engine | Ismail Hasasnah",
    page_icon="🪶",
    layout="centered"
)

# 2. Custom CSS Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .header-container {
        text-align: center;
        padding-top: 10px;
        padding-bottom: 15px;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #10b981 0%, #34d399 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
        margin-bottom: 6px;
    }
    .author-badge {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 8px 22px;
        background: rgba(15, 23, 42, 0.85);
        border-radius: 25px;
        border: 1px solid rgba(16, 185, 129, 0.35);
        display: inline-block;
        margin-top: 6px;
    }
    .author-badge b {
        color: #10b981;
    }
    .badges-grid {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin: 20px 0;
    }
    .badge-item {
        background: #111827;
        border: 1px solid #1f2937;
        color: #cbd5e1;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 0.85rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 24px !important;
    }
    div[data-testid="stSelectbox"] > div {
        background-color: #111827;
        border-radius: 10px;
        border: 1px solid #1f2937;
    }
    .custom-footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #1f2937;
        color: #64748b;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=190)

st.markdown("""
<div class="header-container">
    <h1 class="main-title">ZINO Vision Engine 🪶</h1>
    <div class="author-badge">
        ⚡ Designed & Engineered by <b>Ismail Hasasnah</b>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="badges-grid">
    <span class="badge-item">📐 Rigorous LaTeX Mathematics</span>
    <span class="badge-item">💡 Interactive Feynman Logic</span>
    <span class="badge-item">🌐 Multi-Language (EN / AR / RU)</span>
    <span class="badge-item">🔬 Advanced STEM Deconstruction</span>
</div>
""", unsafe_allow_html=True)

st.caption("Deconstruct complex engineering pages, physics diagrams, and mathematics into clear formulas and intuitive analogies.")

# 4. User Inputs
selected_language = st.selectbox(
    "🌐 Select Target Output Language:",
    ["English", "Arabic", "Russian"]
)

uploaded_file = st.file_uploader("Upload Textbook Page or Mathematical Diagram:", type=["jpg", "jpeg", "png"])

# 5. Core Processing Function
def process_deconstruction(file_obj, lang):
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return "⚠️ **Error:** `GEMINI_API_KEY` is missing in Streamlit Secrets."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        img = Image.open(file_obj)
        prompt = f"""
        You are ZINO Vision Engine using Feynman Methodology.
        Analyze and deconstruct this engineering or mathematical textbook image.
        Target Output Language: {lang}

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
        
        # Dynamic discovery of active vision-capable models
        models_to_try = []
        try:
            for model_info in genai.list_models():
                if 'generateContent' in model_info.supported_generation_methods:
                    models_to_try.append(model_info.name)
        except Exception:
            pass

        # Fallback list if discovery fails
        if not models_to_try:
            models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro"]

        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([prompt, img])
                if response and response.text:
                    return response.text
            except Exception as ex:
                last_error = str(ex)
                continue
                
        return f"⚠️ API Exception: {last_error}"
    except Exception as ex:
        return f"⚠️ Processing Exception: {str(ex)}"

# 6. Execution Trigger
if uploaded_file is not None:
    st.image(uploaded_file.getvalue(), caption="Target Page Preview", use_container_width=True)
    
    if st.button("Deconstruct & Analyze Page 🚀"):
        with st.spinner("Processing page layout and running Feynman vision engine..."):
            result = process_deconstruction(uploaded_file, selected_language)
            st.success("Deconstruction Complete!")
            st.markdown(result)

# 7. Application Footer
st.markdown("""
<div class="custom-footer">
    <b>ZINO AI Systems</b> © 2026 — Developed & Maintained by <b>Ismail Hasasnah</b>
</div>
""", unsafe_allow_html=True)
