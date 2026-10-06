import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي والهندسي
    """
    try:
        # 1. التحقق من وجود مفتاح API
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        elif "GEMINI_API_KEY" in os.environ:
            api_key = os.environ["GEMINI_API_KEY"]
            
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

        # 2. تهيئة مكتبة Gemini
        genai.configure(api_key=api_key)

        # 3. قراءة الصورة
        image = Image.open(image_file)

        # 4. التعليمات الأكاديمية الصارمة (System Prompt)
        system_instruction = """
        أنت محرك ZINO Vision Engine للتحليل الأكاديمي الهندسي الصارم.
        مهمتك الأساسية هي إجراء مسح بصري دقيق (OCR) وقراءة المحتوى المكتوب في الصورة المرفقة فقط!

        قواعد صارمة لمنع الأخطاء والهلوسة:
        1. اقرأ النصوص والمعادلات والأشكال الهندسية المكتوبة في الصورة المرفقة فقط (مثل الإجهاد والاستطالة والأحمال المحورية).
        2. يمنع منعاً باتاً دمج أو إرجاع قوانين غير موجودة بالصورة (مثل الكهرومغناطيسية أو الاهتزازات).
        3. استخدم LaTeX الصحيح للمعادلات:
           - المعادلات المنفصلة بين $$...$$
           - الرموز المدمجة بالنص بين $...$
        4. اكتب التقرير كاملاً ليشمل الأقسام الـ 10 الأكاديمية دون توقف أو اختصار:
           1. استخراج الرموز والمعادلات الرياضية (LaTeX)
           2. التفكيك العلمي والتطبيقي خطوة بخطوة
           3. تشبيه فاينمان التفاعلي المبسط
           4. التحليل البعدي ووحدات القياس (Dimensional Analysis)
           5. الشروط الحدية وحالات الحواف (Boundary Conditions)
           6. الأخطاء الشائعة والمفاهيم الخاطئة (Common Pitfalls)
           7. تطبيقات هندسية في الحياة الواقعية
           8. أسئلة اختبار الفهم الذاتي (Self-Assessment Questions)
           9. ملخص القوانين السريع (Cheat Sheet)
           10. خطة المراجعة والتثبيت (Review Roadmap)
        """

        # 5. استخدام اسم النموذج الحديث المدعوم: gemini-2.5-flash
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        prompt = f"""
        قم بقراءة وتحليل هذه الشريحة الأكاديمية المرفقة بدقة عالية باللغة: {target_language}.
        استخرج القوانين الحقيقية المكتوبة بالصورة فقط وقم بتفكيكها عبر الأقسام الـ 10 كاملة دون حذف.
        """

        # 6. توليد الإجابة
        response = model.generate_content([prompt, image])
        
        return response.text

    except Exception as e:
        return f"❌ **حدث خطأ أثناء الاتصال بالمحرك:** {str(e)}"
