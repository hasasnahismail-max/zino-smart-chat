import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine المطور للسرعة الفائقة والتحليل بأسلوب فاينمان.
    تم الاستغناء عن حلقات الانتظار الطويلة لتفادي تعليق الشاشة.
    """
    try:
        # 1. جلب مفتاح API
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

        # 2. إنشاء عميل الذكاء الاصطناعي
        client = genai.Client(api_key=api_key)

        # 3. معالجة وتجهيز الصورة
        image = Image.open(image_file).convert("RGB")

        # 4. توجيهات النظام (الدقة الأكاديمية + أسلوب فاينمان)
        system_instruction = """
        أنت محرك ZINO Vision Engine المتخصص في التفكيك الأكاديمي الهندسي الصارم وتبسيط المفاهيم بأسلوب فاينمان (Feynman Technique).

        قم بتحليل الشريحة المرفقة بدقة وتنظيم الإجابة لتشمل قسمين أساسيين:

        📍 **القسم الأول: التحليل الأكاديمي والدراسة العلمية الرسمية**
        1. قراءة النصوص والمعادلات المكتوبة بالصورة فقط (OCR دقيق).
        2. استخراج القوانين والرموز والوحدات الفيزيائية.
        3. تنسيق كافة معادلات LaTeX:
           - المعادلات المستقلة بين $$...$$
           - الرموز المدمجة بالنص بين $...$

        📍 **القسم الثاني: تشبيه فاينمان السلس والتفاعلي (Feynman Intuition)**
        1. اشرح المفهوم الهندسي بلغة بسيطة جداً وكأنك تشرح لشخص غير متخصص.
        2. استخدم تشبيهات وأمثلة ملموسة من الحياة اليومية (مثل تشبيه المادة بنوابض ميكروسكوبية، معامل يونغ E بصلابة حبل الغسيل، التخصر Necking بسحب قطعة علكة).
        3. فكك القانون الرياضي إلى معناه الفيزيائي الملموس (دور القوة P، الطول L، المساحة A، ومعامل المرونة E).

        🔴 **قاعدة منع الهلوسة:** لا تضف أي بيانات غير موجودة بالصورة المرفقة.
        """

        prompt = f"قم بقراءة وتحليل هذه الشريحة الأكاديمية بالكامل بلغة: {target_language}. اربط الشرح الأكاديمي بقسم فاينمان المبسط."

        # 5. طلب أسرع نموذج مباشر دون انتظار
        models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash']
        
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, image],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2
                    )
                )
                if response and response.text:
                    return response.text
            except Exception:
                continue # الانتقال الفوري للنموذج التالي بدون وقت انتظار time.sleep

        return "⚠️ **تعذر الاتصال بالمحرك في هذه اللحظة، يرجى إعادة الضغط على الزر مرة أخرى.**"

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع:** `{str(general_error)}`"
