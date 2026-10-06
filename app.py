import streamlit as st
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="ZINO Vision Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. القاموس متعدد اللغات
I18N = {
    "Arabic": {
        "title": "محرك زينو للرؤية الأكاديمية 🪶",
        "badge": "⚡ تصميم وهندسة: إسماعيل حساسنة",
        "pill_math": "🧮 10 أقسام علمية صارمة",
        "pill_feynman": "📜 12 شرطاً للتدقيق والأمانة",
        "pill_lang": "🌐 دعم عربي / EN / RU",
        "pill_stem": "🔬 تفكيك واستخراج المعادلات والوحدات",
        "description": "تفكيك صفحات الكتب والمحاضرات وفق هيكل 10 أقسام أكاديمية و 12 شرطاً للأمانة والدقة العلمية.",
        "select_lang_label": "🌐 اختر لغة التحليل والواجهة المستهدفة:",
        "upload_label": "📤 ارفع صفحة كتاب، محاكات، أو مادة دراسية:",
        "upload_help": "يدعم PNG, JPG, JPEG • حتى 200MB",
        "analyze_btn": "🚀 تفكيك المحتوى وفق الأقسام الـ 10 والشروط الـ 12",
        "spinner": "جاري التفكيك والتحقيق من المعادلات وفق القواعد الـ 12...",
        "results_header": "📊 نتائج التفكيك والتحليل الأكاديمي الصارم:",
        "footer": "نظم زينو للذكاء الاصطناعي © 2026 — إسماعيل حساسنة",
        "uploaded_caption": "الصورة المرفوعة للتحليل",
        "dir": "rtl"
    },
    "English": {
        "title": "ZINO Vision Engine 🪶",
        "badge": "⚡ Designed & Engineered by Ismail Hasasnah",
        "pill_math": "🧮 10 Strict Academic Sections",
        "pill_feynman": "📜 12 Rules of Verification",
        "pill_lang": "🌐 Multi-Language (EN / AR / RU)",
        "pill_stem": "🔬 Formula & Unit Extraction",
        "description": "Deconstruct lecture slides and textbook pages strictly following 10 structural sections and 12 accuracy guidelines.",
        "select_lang_label": "🌐 Select Output & UI Language:",
        "upload_label": "📤 Upload Textbook Page or Diagram:",
        "upload_help": "Supports PNG, JPG, JPEG • up to 200MB",
        "analyze_btn": "🚀 Analyze according to 10 Sections & 12 Rules",
        "spinner": "Deconstructing and verifying formulas against strict rules...",
        "results_header": "📊 Strict Academic Deconstruction Results:",
        "footer": "ZINO AI Systems © 2026 — Ismail Hasasnah",
        "uploaded_caption": "Uploaded Image",
        "dir": "ltr"
    },
    "Russian": {
        "title": "ZINO Vision Engine 🪶",
        "badge": "⚡ Разработка: Исмаил Хасасна",
        "pill_math": "🧮 10 Академических Разделов",
        "pill_feynman": "📜 12 Строгих Правил",
        "pill_lang": "🌐 Языки (AR / EN / RU)",
        "pill_stem": "🔬 Извлечение Формул и Единиц",
        "description": "Анализ учебных материалов по 10 разделам и 12 правилам научной точности.",
        "select_lang_label": "🌐 Выберите язык анализа и интерфейса:",
        "upload_label": "📤 Загрузите страницу или диаграмму:",
        "upload_help": "PNG, JPG, JPEG • До 200МБ",
        "analyze_btn": "🚀 Начать анализ по 10 разделам",
        "spinner": "Анализ и проверка уравнений по 12 правилам...",
        "results_header": "📊 Результаты академического анализа:",
        "footer": "ZINO AI Systems © 2026 — Исмаил Хасасна",
        "uploaded_caption": "Загруженное изображение",
        "dir": "ltr"
    }
}

# 3. حفظ خيار اللغة في الجلسة
if "target_lang" not in st.session_state:
    st.session_state["target_lang"] = "Arabic"

lang_options = {
    "Arabic": "العربية (Arabic)",
    "English": "English",
    "Russian": "Русский (Russian)"
}

selected_lang = st.selectbox(
    "🌐 اختر لغة التحليل / Select Language:",
    options=list(lang_options.keys()),
    format_func=lambda x: lang_options[x],
    index=list(lang_options.keys()).index(st.session_state["target_lang"])
)

st.session_state["target_lang"] = selected_lang
txt = I18N[selected_lang]

# 4. التنسيق البرمجي (CSS)
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #4A1525 !important;
        color: #FFFFFF !important;
        direction: {txt['dir']};
    }}
    div.block-container {{ padding-top: 1.2rem; max-width: 850px; }}
    .main-title {{
        text-align: center; font-size: 2.6rem; font-weight: 900;
        background: linear-gradient(90deg, #00FF9D 0%, #00D4FF 50%, #FFC107 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .developer-badge {{
        background: rgba(255, 215, 0, 0.15); border: 2px solid #FFD700;
        padding: 6px 18px; border-radius: 20px; text-align: center;
        color: #FFE57F !important; font-weight: 800; margin: 8px auto 20px auto; width: fit-content;
    }}
    .pill-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }}
    .pill-card {{ padding: 14px; border-radius: 12px; font-weight: 700; text-align: center; }}
    .pill-math {{ background: rgba(0, 255, 157, 0.2); border: 2px solid #00FF9D; color: #A7FFEB !important; }}
    .pill-feynman {{ background: rgba(255, 193, 7, 0.2); border: 2px solid #FFC107; color: #FFF59D !important; }}
    .pill-lang {{ background: rgba(0, 212, 255, 0.2); border: 2px solid #00D4FF; color: #E0F7FA !important; }}
    .pill-stem {{ background: rgba(255, 42, 133, 0.2); border: 2px solid #FF2A85; color: #FF80AB !important; }}
    
    div[data-baseweb="select"] > div {{ background-color: #2D0B16 !important; border: 2px solid #00D4FF !important; }}
    div[data-baseweb="select"] * {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    
    .stButton > button {{
        background: linear-gradient(90deg, #00FF9D 0%, #00D4FF 100%) !important;
        color: #1A000A !important; font-weight: 900 !important; font-size: 1.15rem !important;
        border-radius: 12px !important; width: 100% !important; border: none !important;
    }}
    .footer {{ text-align: center; font-size: 0.9rem; color: #E2E8F0; margin-top: 35px; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 18px; }}
    </style>
""", unsafe_allow_html=True)

# 5. الواجهة الرئيسية
st.markdown(f'<div class="main-title">{txt["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="developer-badge">{txt["badge"]}</div>', unsafe_allow_html=True)

st.markdown(f'''
<div class="pill-grid">
    <div class="pill-card pill-math">{txt["pill_math"]}</div>
    <div class="pill-card pill-feynman">{txt["pill_feynman"]}</div>
    <div class="pill-card pill-lang">{txt["pill_lang"]}</div>
    <div class="pill-card pill-stem">{txt["pill_stem"]}</div>
</div>
''', unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center; background:rgba(255,255,255,0.08); padding:12px; border-radius:10px; margin-bottom:20px;">{txt["description"]}</div>', unsafe_allow_html=True)

# 6. قسم رفع وتحليل الصور
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
                analysis_result = f"Error: {str(e)}"
            
            st.markdown("---")
            st.markdown(f'### {txt["results_header"]}')
            st.markdown(analysis_result)

# 7. التذييل
st.markdown(f'<div class="footer">{txt["footer"]}</div>', unsafe_allow_html=True)
