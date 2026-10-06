import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي والهندسي
    """
    try:
        # 1. جلب مفتاح API
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
            
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

        # 2. إنشاء عميل الذكاء الاصطناعي
        client = genai.Client(api_key=api_key)

        # 3. فتح وقراءة الصورة
        image = Image.open(image_file)

        # 4. التوجيهات الأكاديمية الصارمة
        system_instruction = """
        أنت محرك ZINO Vision Engine للتحليل الأكاديمي الهندسي الصارم.
        مهمتك الأساسية هي إجراء مسح بصري دقيق (OCR) وقراءة المحتوى المكتوب في الصورة المرفقة فقط!

        قواعد صارمة لمنع الأخطاء والهلوسة:
        1. اقرأ النصوص والمعادلات والأشكال الهندسية المكتوبة في الصورة المرفقة فقط (مثل الإجهاد، الأحمال المحورية، والاستطالة).
        2. يمنع منعاً باتاً دمج أو إرجاع قوانين غير موجودة بالصورة.
        3. استخدم LaTeX الصحيح للمعادلات:
           - المعادلات المنفصلة بين $$...$$
           - الرموز المدمجة بالنص بين $...$
        4. اكتب التقرير كاملاً ليشمل الأقسام الـ 10 الأكاديمية دون توقف أو اختصار.
        """

        prompt = f"""
        قم بقراءة وتحليل هذه الشريحة الأكاديمية المرفقة بدقة عالية باللغة: {target_language}.
        استخرج القوانين الحقيقية المكتوبة بالصورة فقط وقم بتفكيكها عبر الأقسام الـ 10 كاملة دون حذف.
        """

        # 5. استدعاء النموذج الجديد الموصى به من جوجل: gemini-3.8-flash
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )
        
        return response.text

    except Exception as e:
        return f"❌ **حدث خطأ أثناء الاتصال بالمحرك:** {str(e)}"
