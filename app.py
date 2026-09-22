import streamlit as st
from ai_engine import deconstruct_engineering_page

st.set_page_config(page_title="ZINO Feynman Engine", page_icon="🚀", layout="centered")

st.title("🚀 ZINO Feynman Vision Engine")
st.subheader("تفكيك الصفحات الهندسية المعقدة إلى رياضيات دقيقة وتشبيهات مبسطة")

# Language Selector
selected_language = st.selectbox(
    "🌐 اختر لغة التحليل / Выберите язык анализа / Select Output Language:",
    ["العربية", "Русский", "English"]
)

uploaded_file = st.file_uploader("ارفع صورة من كتاب هندسة أو رياضيات", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Selected Page", use_column_width=True)
    
    if st.button("Deconstruct & Simplify Page 🚀"):
        with st.spinner("جاري تحليل الصفحة وتطبيق منهجية فاينمان..."):
            result = deconstruct_engineering_page(uploaded_file, language=selected_language)
            st.success("Deconstruction Complete!")
            st.markdown(result)
