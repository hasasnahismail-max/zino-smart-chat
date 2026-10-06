import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي والهندسي المتقدم.
    يتضمن نظام التبديل التلقائي بين النماذج لتفادي انقطاع الخدمة عند الضغط العالي على الخوادم.
    """
    try:
        # 1. جلب مفتاح API بأمان من Secrets أو متغيرة البيئة
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى التأكد من إضافته في Streamlit Secrets."

        # 2. إنشاء عميل الذكاء الاصطناعي
        client = genai.Client(api_key=api_key)

        # 3. قراءة وتجهيز الصورة وتعديل نمط الألوان إلى RGB بأمان
        image = Image.open(image_file).convert("RGB")

        # 4. إعداد التوجيهات النظامية والبرومبت الأكاديمي
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

        # 5. قائمة النماذج المعتمدة بالترتيب حسب الأحدث والأسرع
        models_to_try = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]

        last_error = None

        # 6. المحاولة التلقائية عبر النماذج بالتتابع
        for model_name in models_to_try:
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
                # الانتقال التجريبي للنموذج التالي فوراً
                continue

        # في حال استنفاد كافة النماذج مع وجود خطأ في الاتصال
        return (
            "⚠️ **تنبيه:** تعذر الاتصال بخوادم Google حالياً بسبب الضغط المؤقت على الخدمة.\n\n"
            f"**تفاصيل الخطأ:** `{str(last_error)}`\n\n"
            "💡 **حل مقترح:** يرجى إعادة الضغط على زر التفكيك بعد بضع ثوانٍ."
        )

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع أثناء المعالجة:** `{str(general_error)}`"
