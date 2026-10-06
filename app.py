import streamlit as st
from PIL import Image

# 1. إعداد الصفحة والعرض
st.set_page_config(
    page_title="ZINO Vision Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. قاموس الترجمة الفورية الديناميكية لتفاعل الواجهة بالكامل مع اللغة المختارة
I18N = {
    "Arabic": {
        "title": "محرك زينو للرؤية الذكية 🪶",
        "badge": "⚡ تصميم وهندسة: إسماعيل حساسنة",
        "pill_math": "📐 رياضيات LaTeX دقيقة وصارمة",
        "pill_feynman": "💡 منطق فاينمان التفاعلي المبسط",
        "pill_lang": "🌐 متعدد اللغات (عربي / EN / RU)",
        "pill_stem": "🔬 تفكيك وهندسة المفاهيم العلمية STEM",
        "description": "تفكيك صفحات الكتب العلمية، المخططات الهندسية، ومسائل الفيزياء إلى معادلات صارمة وتشبهات فاينمان المبسطة.",
        "select_lang_label": "🌐 اختر لغة التطبيق والتحليل المستهدفة:",
        "upload_label": "📤 ارفع صفحة من كتاب دراسي أو مخططاً علمياً/هندسياً:",
        "upload_help": "الحد الأقصى 200MB • يدعم PNG, JPG, JPEG",
        "analyze_btn": "🚀 تفكيك وتحليل المحتوى العلمي والتطبيقي",
        "spinner": "جاري تحليل قوانين الفيزياء، المعادلات الرياضية، والنماذج الهندسية بأعلى دقة...",
        "results_header": "📊 نتائج التفكيك والتحليل العلمي:",
        "footer": "نظم زينو للذكاء الاصطناعي © 2026 — تطوير وصيانة إسماعيل حساسنة",
        "uploaded_caption": "الصورة المرفوعة للتحليل",
        "dir": "rtl"
    },
    "English": {
        "title": "ZINO Vision Engine 🪶",
        "badge": "⚡ Designed & Engineered by Ismail Hasasnah",
        "pill_math": "📐 Rigorous LaTeX Mathematics",
        "pill_feynman": "💡 Interactive Feynman Logic",
        "pill_lang": "🌐 Multi-Language (EN / AR / RU)",
        "pill_stem": "🔬 Advanced STEM Deconstruction",
        "description": "Deconstruct complex engineering pages, physics diagrams, and mathematics into clear formulas and intuitive analogies.",
        "select_lang_label": "🌐 Select Target Output & UI Language:",
        "upload_label": "📤 Upload Textbook Page or Mathematical Diagram:",
        "upload_help": "200MB per file • JPG, PNG, JPEG",
        "analyze_btn": "🚀 Deconstruct & Analyze STEM Content",
        "spinner": "Analyzing physics, mathematics, and engineering models with rigorous precision...",
        "results_header": "📊 Deconstruction Results & Analysis:",
        "footer": "ZINO AI Systems © 2026 — Developed & Maintained by Ismail Hasasnah",
        "uploaded_caption": "Uploaded Textbook Page / Diagram",
        "dir": "ltr"
    },
    "Russian": {
        "title": "ZINO Vision Engine 🪶",
        "badge": "⚡ Разработано и спроектировано Исмаилом Хасасна",
        "pill_math": "📐 Строгая математика LaTeX",
        "pill_feynman": "💡 Интерактивная логика Фейнмана",
        "pill_lang": "🌐 Многоязычный (AR / EN / RU)",
        "pill_stem": "🔬 Продвинутый STEM-анализ",
        "description": "Преобразование сложных инженерных схем, физических диаграмм и математики в четкие формулы и наглядные аналогии.",
        "select_lang_label": "🌐 Выберите язык интерфейса и анализа:",
        "upload_label": "📤 Загрузите страницу учебника или научную диаграмму:",
        "upload_help": "До 200МБ • JPG, PNG, JPEG",
        "analyze_btn": "🚀 Начать деконструкцию и STEM-анализ",
        "spinner": "Анализ физики, математики и инженерных моделей с высокой точностью...",
        "results_header": "📊 Результаты анализа и деконструкции:",
        "footer": "ZINO AI Systems © 2026 — Разработка и поддержка: Исмаил Хасасна",
        "uploaded_caption": "Загруженное изображение",
        "dir": "ltr"
    }
}

# 3. إدارة حالة اللغة المحددة
if "target_lang" not in st.session_state:
    st.session_state["target_lang"] = "Arabic"

lang_options = {
    "Arabic": "العربية (Arabic)",
    "English": "English",
    "Russian": "Русский (Russian)"
}

# القائمة المنسدلة لاختيار اللغة في بداية الواجهة لتتفاعل مباشرة
selected_lang = st.selectbox(
    "🌐 Select Target Output & UI Language / اختر لغة التطبيق والتحليل:",
    options=list(lang_options.keys()),
    format_func=lambda x: lang_options[x],
    index=list(lang_options.keys()).index(st.session_state["target_lang"])
)

st.session_state["target_lang"] = selected_lang
txt = I18N[selected_lang]

# 4. CSS المتقدم: حل مشكلة الخط الداكن كلياً وإبراز الأيقونات بألوان نيون متباينة وواضحة
st.markdown(f"""
    <style>
    /* خلفية التطبيق باللون الخمري الأصيل المبهج */
    .stApp {{
        background-color: #4A1525 !important;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: {txt['dir']};
    }}

    div.block-container {{
        padding-top: 1.2rem;
        max-width: 850px;
    }}

    /* العنوان الرئيسي بتدرج زمردي وسيان وذهبي */
    .main-title {{
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00FF9D 0%, #00D4FF 50%, #FFC107 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        filter: drop-shadow(0px 4px 12px rgba(0, 0, 0, 0.6));
    }}

    /* شارة المطور الذهبية الملكية */
    .developer-badge {{
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.22) 0%, rgba(255, 255, 255, 0.08) 100%);
        border: 2px solid #FFD700;
        padding: 8px 22px;
        border-radius: 25px;
        text-align: center;
        font-weight: 800;
        color: #FFE57F !important;
        margin: 8px auto 25px auto;
        width: fit-content;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }}

    /* بطاقات المميزات بألوان نيون متباينة وفتاكة */
    .pill-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
        margin-bottom: 25px;
    }}

    @media (max-width: 600px) {{
        .pill-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    .pill-card {{
        padding: 16px 20px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 0.98rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(12px);
    }}

    /* 1. رياضيات - نيون زمردي */
    .pill-math {{
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.25) 0%, rgba(0, 100, 60, 0.4) 100%);
        border: 2px solid #00FF9D;
        color: #A7FFEB !important;
        box-shadow: 0 4px 18px rgba(0, 255, 157, 0.35);
    }}
    .pill-math:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 255, 157, 0.6);
    }}

    /* 2. منطق فاينمان - ذهبي كهرماني */
    .pill-feynman {{
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.28) 0%, rgba(150, 90, 0, 0.4) 100%);
        border: 2px solid #FFC107;
        color: #FFF59D !important;
        box-shadow: 0 4px 18px rgba(255, 193, 7, 0.35);
    }}
    .pill-feynman:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 193, 7, 0.6);
    }}

    /* 3. اللغات - سيان كهربائي */
    .pill-lang {{
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.28) 0%, rgba(0, 80, 150, 0.4) 100%);
        border: 2px solid #00D4FF;
        color: #E0F7FA !important;
        box-shadow: 0 4px 18px rgba(0, 212, 255, 0.35);
    }}
    .pill-lang:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.6);
    }}

    /* 4. هندسة STEM - ماجنتا وبنفسجي مكهرب */
    .pill-stem {{
        background: linear-gradient(135deg, rgba(255, 42, 133, 0.3) 0%, rgba(120, 0, 60, 0.4) 100%);
        border: 2px solid #FF2A85;
        color: #FF80AB !important;
        box-shadow: 0 4px 18px rgba(255, 42, 133, 0.35);
    }}
    .pill-stem:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 42, 133, 0.6);
    }}

    /* صندوق الوصف الفرعي */
    .sub-description {{
        text-align: center;
        color: #F8F9FA !important;
        font-size: 1.05rem;
        margin-bottom: 25px;
        line-height: 1.6;
        background: rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }}

    /* إجبار إظهار نص القائمة المنسدلة باللون الأبيض الناصع والواضح جداً */
    div[data-baseweb="select"] > div {{
        background-color: #2D0B16 !important;
        border: 2px solid #00D4FF !important;
        border-radius: 12px !important;
    }}
    div[data-baseweb="select"] * {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}
    div[data-baseweb="menu"] {{
        background-color: #3D0E1E !important;
        border: 1.5px solid #00D4FF !important;
    }}
    div[data-baseweb="menu"] li {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="menu"] li:hover {{
        background-color: #611A30 !important;
        color: #00FF9D !important;
    }}
    
    div.stSelectbox label p {{
        color: #00D4FF !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }}

    /* صندوق رفع الملفات */
    .stFileUploader {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 18px;
        border: 2px dashed #00FF9D;
    }}
    
    div.stFileUploader label p {{
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }}

    /* زر التحليل البرّاق والتفاعلي */
    .stButton > button {{
        background: linear-gradient(90deg, #00FF9D 0%, #00D4FF 100%) !important;
        color: #1A000A !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.8rem !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 22px rgba(0, 255, 157, 0.5) !important;
        transition: all 0.3s ease !important;
    }}

    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.7) !important;
    }}

    /* التذييل */
    .footer {{
        text-align: center;
        font-size: 0.9rem;
        color: #E2E8F0;
        margin-top: 45px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 22px;
        font-weight: 600;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. عرض عناصر الواجهة المترجمة ديناميكياً بحسب اللغة المختارة
st.markdown(f'<div class="main-title">{txt["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="developer-badge">{txt["badge"]}</div>', unsafe_allow_html=True)

# عرض البطاقات الأربعة بألوانها المتباينة الفتاكة
st.markdown(f'''
<div class="pill-grid">
    <div class="pill-card pill-math">{txt["pill_math"]}</div>
    <div class="pill-card pill-feynman">{txt["pill_feynman"]}</div>
    <div class="pill-card pill-lang">{txt["pill_lang"]}</div>
    <div class="pill-card pill-stem">{txt["pill_stem"]}</div>
</div>
''', unsafe_allow_html=True)

st.markdown(f'<div class="sub-description">{txt["description"]}</div>', unsafe_allow_html=True)

st.write("---")

# 6. قسم رفع الصور ومخططات العلوم
st.markdown(f'### {txt["upload_label"]}')
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], help=txt["upload_help"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=txt["uploaded_caption"], use_column_width=True)
    
    if st.button(txt["analyze_btn"]):
        with st.spinner(txt["spinner"]):
            try:
                from ai_engine import process_stem_analysis
                analysis_result = process_stem_analysis(uploaded_file, selected_lang)
            except Exception as e:
                analysis_result = f"Error executing analysis: {str(e)}"
            
            st.markdown("---")
            st.markdown(f'### {txt["results_header"]}')
            st.markdown(analysis_result)

# 7. التذييل المترجم
st.markdown(f'<div class="footer">{txt["footer"]}</div>', unsafe_allow_html=True)
