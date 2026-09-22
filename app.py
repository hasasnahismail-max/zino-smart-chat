import os
import streamlit as st

# 1. Page Configuration & Icon
st.set_page_config(
    page_title="ZINO Vision Engine | Ismail Hasasnah",
    page_icon="🪶",
    layout="centered"
)

# 2. Custom CSS Styles matching Cyber Emerald & Gold Theme
st.markdown("""
<style>
    /* Global App Background & Typography */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Header Container */
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
        letter-spacing: -0.5px;
    }
    
    /* Author Badge */
    .author-badge {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 8px 22px;
        background: rgba(15, 23, 42, 0.85);
        border-radius: 25px;
        border: 1px solid rgba(16, 185, 129, 0.35);
        display: inline-block;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
        margin-top: 6px;
    }
    
    .author-badge b {
        color: #10b981;
    }

    /* Feature Badges */
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
        font-weight: 500;
    }

    /* Primary Launch Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5);
    }

    /* Selectbox Input */
    div[data-testid="stSelectbox"] > div {
        background-color: #111827;
        border-radius: 10px;
        border: 1px solid #1f2937;
    }

    /* Footer */
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

# Safe Engine Import
try:
    import ai_engine
except Exception as import_err:
    st.error(f"Error loading AI Engine module: {import_err}")
    st.stop()

# 3. Logo Display & Header
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

# 4. Feature Badges
st.markdown("""
<div class="badges-grid">
    <span class="badge-item">📐 Rigorous LaTeX Mathematics</span>
    <span class="badge-item">💡 Interactive Feynman Logic</span>
    <span class="badge-item">🌐 Multi-Language (EN / AR / RU)</span>
    <span class="badge-item">🔬 Advanced STEM Deconstruction</span>
</div>
""", unsafe_allow_html=True)

st.caption("Deconstruct complex engineering pages, physics diagrams, and mathematics into clear formulas and intuitive analogies.")

# 5. Language Selection Dropdown
selected_language = st.selectbox(
    "🌐 Select Target Output Language:",
    ["English", "Arabic", "Russian"]
)

# 6. File Uploader & Execution
uploaded_file = st.file_uploader("Upload Textbook Page or Mathematical Diagram:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file.getvalue(), caption="Target Page Preview", use_container_width=True)
    
    if st.button("Deconstruct & Analyze Page 🚀"):
        with st.spinner("Processing page layout and running Feynman vision engine..."):
            result = ai_engine.deconstruct_engineering_page(uploaded_file, language=selected_language)
            st.success("Deconstruction Complete!")
            st.markdown(result)

# 7. Copyright Footer
st.markdown("""
<div class="custom-footer">
    <b>ZINO AI Systems</b> © 2026 — Developed & Maintained by <b>Ismail Hasasnah</b>
</div>
""", unsafe_allow_html=True)
