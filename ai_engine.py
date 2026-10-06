import os
import io
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine المعالج لقراءة بكسلات الصورة الحقيقية 
    واستخراج كافة الأقسام الـ 10 دون هلوسة أو نص افتراضي ثابت.
    """
    try:
        # 1. جلب مفتاح API من Streamlit Secrets أو متغيرات البيئة
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        elif "GEMINI_API_KEY" in os.environ:
            api_key = os.environ["GEMINI_API_KEY"]
            
        # إذا لم يتم العثور على المفتاح، أظهر رسالة تنبيه صريحة بدلاً من طباعة نص وهمي
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافة المفتاح في إعدادات Streamlit Secrets."

        # 2. إنشاء عميل Gemini باستخدام المفتاح المباشر
        client = genai.Client(api_key=api_key)
        
        # 3. تحويل الصورة المرفوعة إلى Bytes صريحة لضمان إرسالها للنموذج
        image = Image.open(image_file)
        img_byte_arr = io.BytesIO()
        img_format = image.format if image.format else 'PNG'
        image.save(img_byte_arr, format=img_format)
        image_bytes = img_byte_arr.getvalue()

        # 4. تعليمات صارمة جداً لقراءة المحتوى الفعلي للصورة فقط
        system_instruction = """
        أنت محرك ZINO Vision Engine للتحليل الأكاديمي الهندسي الصارم.
        مهمتك الأساسية هي إجراء مسح بصري دقيق (OCR) وقراءة المحتوى المكتوب في الصورة المرفقة فقط!

        قواعد صارمة لمنع الأخطاء والحلول الوهمية:
        1. اقرأ النصوص والمعادلات والأشكال الهندسية المكتوبة في الصورة المرفقة فقط.
        2. يمنع منعاً باتاً إرجاع أي نص افتراضي مخزن مسبقاً أو دمج قوانين غير موجودة في الصورة (مثل قانون غاوس أو الاهتزازات أو Dampers إذا كانت الصورة عن موضوع آخر).
        3. استخدم LaTeX الصحيح للمعادلات:
           - المعادلات المنفصلة بين $$...$$
           - الرموز المدمجة بالنص بين $...$
        4. يجب عليك كتابة التقرير كاملاً ليشمل الأقسام الـ 10 الأكاديمية دون توقف أو اختصار:
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

        prompt = f"""
        قم بقرائة وتحليل هذه الشريحة الأكاديمية المرفقة بدقة عالية باللغة: {target_language}.
        استخرج القوانين الحقيقية المكتوبة بالصورة وقم بتفكيكها عبر الأقسام الـ 10 كاملة دون حذف أي قسم.
        """

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=f"image/{img_format.lower()}"
        )

        # 5. استدعاء النموذج معرفع سقف المخرجات لمنع الانقطاع
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                max_output_tokens=8192
            )
        )
        
        return response.text

    except Exception as e:
        return f"❌ **حدث خطأ أثناء الاتصال بالمحرك:** {str(e)}"
