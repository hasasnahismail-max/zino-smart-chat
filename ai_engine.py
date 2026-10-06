import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي والهندسي المتقدم.
    يعتمد نموذج gemini-3.8-flash المعتمد رسمياً مع نظام إعادة المحاولة عند الضغط.
    """
    try:
        # 1. جلب مفتاح API بأمان
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى التأكد من إضافته في Streamlit Secrets."

        # 2. إنشاء عميل الذكاء الاصطناعي
        client = genai.Client(api_key=api_key)

        # 3. قراءة وتجهيز الصورة
        image = Image.open(image_file).convert("RGB")

        # 4. التوجيه الأكاديمي
        system_instruction = """
        أنت محرك ZINO Vision Engine للتحليل الأكاديمي والهندسي الصارم.
        مهمتك الأساسية هي قراءة واستخراج المحتوى البصري والأكاديمي من الشريحة/الصورة المرفقة بدقة متناهية (OCR دقيق).

        قواعد التحليل والأمان الأكاديمي:
        1. استخرج النص والمعادلات والأشكال الهندسية الموجودة في الصورة المرفقة فقط.
        2. يمنع منعاً باتاً دمج أو اختراع قوانين أو بيانات غير موجودة بالصورة (Zero Hallucination).
        3. قم بتنسيق المعادلات الرياضية باستخدام LaTeX بشكل محكم:
           - المعادلات المستقلة في سطر خاص استخدم: $$...$$
           - المتغيرات والرموز المدمجة في النص استخدم: $...$
        4. قدم تقريراً شاملاً ومنظماً ينظم التحليل بدقة عالية.
        """

        prompt = f"""
        قم بقراءة وتحليل هذه الشريحة الأكاديمية المرفقة بدقة متناهية باللغة: {target_language}.
        استخرج النص والقوانين والمفاهيم بدقة واشرحها تفصيلياً عبر التنسيق الأكاديمي الشامل.
        """

        # 5. استخدام النموذج المعتمد حصراً مع إعادة المحاولة في حال وجود ضغط (Retry Logic)
        model_name = 'gemini-3.8-flash'
        max_retries = 3
        last_error = None

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, image],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.1
                    )
                )
                
                if response and response.text:
                    return response.text
                    
            except Exception as e:
                last_error = e
                # الانتظار لمدة ثانيتين قبل إعادة المحاولة تلقائياً في حال وجود ضغط 503
                time.sleep(2)

        return f"⚠️ **السيرفر مشغول حالياً، يرجى الضغط مرة أخرى بعد ثوانٍ قليلة.**\nتفاصيل: `{str(last_error)}`"

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع أثناء المعالجة:** `{str(general_error)}`"
