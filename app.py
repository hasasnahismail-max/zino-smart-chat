import streamlit as st
from PIL import Image
import os

# 1. إعداد الصفحة وتكوين العرض
st.set_page_config(
    page_title="ZINO Vision Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تصميم الواجهة بالكامل وتطبيق الخلفية الخمرية الأصيلة (#4A1525) وتنسيق الأزرار
st.markdown("""
    <style>
    /* خلفية التطبيق باللون الخمري الأصيل والمبهج */
    .stApp {
        background-color: #4A1525 !important;
        color: #F8F9FA !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    div.block-container {
        padding-top: 2rem;
        max-width: 800px;
    }

    /* عنوان التطبيق الرئيسي */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #00FF88 !important;
        margin-bottom: 0px;
    }

    /* شارة المطور */
    .developer-badge {
        background-color: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 10px 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        color: #00FF88;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* أزرار ومميزات النظام (Feature Pills) المطابقة للصورة */
    .feature-pill {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 15px;
        border-radius: 20px;
        text-align: center;
        font-size: 0.95rem;
        color: #F8F9FA;
        margin-bottom: 10px;
        font-weight: 500;
    }

    /* تخصيص القائمة المنسدلة للغة */
    div.stSelectbox > div > div {
        background-color: #5D1A2E !important;
        color: #FFFFFF !important;
        border: 1px solid #7A223D !important;
        border-radius: 8px;
    }

    div.stSelectbox label {
        color: #F8F9FA !important;
        font-weight: 600;
    }

    /* صندوق رفع الملفات */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        border: 2px dashed rgba(255, 255, 255, 0.2);
    }

    /* زر التحليل والتنفيذ */
    .stButton > button {
        background-color: #00FF88 !important;
        color: #4A1525 !important;
        font-weight: 700;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #00cc6a !important;
        box-shadow: 0 6px 16px rgba(0, 255, 136, 0.5);
    }

    /* العناوين والنصوص العامة */
    h1, h2, h3, p, label, span, .stMarkdown {
        color: #F8F9FA !important;
    }

    .sub-description {
        text-align: center;
        color: #E2E8F0;
        font-size: 1.05rem;
        margin-bottom: 25px;
        line-height: 1.5;
    }

    /* التذييل (Footer) */
    .footer {
        text-align: center;
        font-size: 0.85em;
        color: #CBD5E1;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ترويسة وشعار التطبيق
st.markdown('<div class="main-title">ZINO Vision Engine 🪶</div>', unsafe_allow_html=True)
st.markdown('<div class="developer-badge">⚡ Designed & Engineered by Ismail Hasasnah</div>', unsafe_allow_html=True)

# 4. بطاقات المميزات الأربعة الظاهرة في الواجهة
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="feature-pill">📐 Rigorous LaTeX Mathematics</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-pill">🌐 Multi-Language (EN / AR / RU)</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-pill">💡 Interactive Feynman Logic</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-pill">🔬 Advanced STEM Deconstruction</div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="sub-description">Deconstruct complex engineering pages, physics diagrams, and mathematics into clear formulas and intuitive analogies.</div>', unsafe_allow_html=True)

# 5. قائمة اختيار لغة الإخراج (مع ضمان الحفظ الفعلي لحل مشكلة تحويل اللغة)
languages = {
    "Arabic": "العربية (Arabic)",
    "English": "English",
    "Russian": "Русский (Russian)"
}

selected_lang_key = st.selectbox(
    "🌐 Select Target Output Language:",
    list(languages.keys()),
    format_func=lambda x: languages[x]
)

# حفظ اللغة المختار بشكل دقيق في الجلسة ليقرأها محرك الذكاء الاصطناعي
st.session_state["target_lang"] = selected_lang_key

st.write("---")

# 6. قسم رفع الملفات والصفحات
st.markdown("### 📤 Upload Textbook Page or Mathematical Diagram")
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], help="200MB per file • JPG, PNG")

if uploaded_file is not None:
    # عرض معاينة الصورة المرفوعة
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Textbook Page / Diagram", use_column_width=True)
    
    # زر تشغيل التحليل
    if st.button("🚀 Deconstruct & Analyze STEM Content"):
        with st.spinner("Analyzing physics, mathematics, and engineering models with rigorous precision..."):
            
            # استدعاء دالة التحليل المتقدمة من ملف ai_engine
            try:
                from ai_engine import process_stem_analysis
                analysis_result = process_stem_analysis(uploaded_file, st.session_state.get("target_lang", "Arabic"))
            except Exception as e:
                analysis_result = f"Error executing analysis engine: {str(e)}"
            
            st.markdown("---")
            st.markdown("### 📋 Deconstruction Results & Analysis:")
            st.markdown(analysis_result)

# 7. تذييل حقوق النشر
st.markdown('<div class="footer">ZINO AI Systems © 2026 — Developed & Maintained by Ismail Hasasnah</div>', unsafe_allow_html=True)
