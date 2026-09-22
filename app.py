import streamlit as st
import ai_engine

st.set_page_config(
    page_title="ZINO Feynman Engine",
    page_icon="📐",
    layout="wide"
)

st.title("📐 ZINO Feynman Vision Engine")
st.caption("Engineered by Ismail Hasasneh — STEM Textbook Page Deconstruction Platform")

st.markdown("""
> **How to use:** Capture or upload any page from an engineering, mathematics, or physics textbook. The engine will instantly break down the complex formulas into LaTeX math and simple Feynman-style analogies.
""")

# Input source selection
input_mode = st.radio(
    "Select Input Source:",
    ["📸 Live Camera Capture", "📁 Upload Image File"],
    horizontal=True
)

uploaded_page = None

if input_mode == "📸 Live Camera Capture":
    uploaded_page = st.camera_input("Point camera at textbook page and click capture")
else:
    uploaded_page = st.file_uploader("Upload page image:", type=["png", "jpg", "jpeg"])

if uploaded_page:
    st.image(uploaded_page, caption="Selected Page", width=400)
    
    if st.button("Deconstruct & Simplify Page 🚀", use_container_width=True):
        with st.spinner("Deconstructing mathematical formulas into Feynman analogies..."):
            result = ai_engine.deconstruct_engineering_page(uploaded_page)
            st.success("Deconstruction Complete!")
            st.markdown(result)
