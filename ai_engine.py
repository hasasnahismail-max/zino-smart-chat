import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي وتفكيك المفاهيم بأسلوب فاينمان.
    معالج بالكامل لمواجهة أخطاء الضغط (503) واستنفاد الحصة (429).
    """
    try:
        # 1. التحقق من وجود مفتاح API
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

        # 2. إنشاء عميل SDK
        client = genai.Client(api_key=api_key)

        # 3. قراءة وتجهيز الصورة
        image = Image.open(image_file).convert("RGB")

        # 4. توجيهات النظام (الدقة الأكاديمية + أسلوب فاينمان)
        system_instruction = """
        أنت محرك ZINO Vision Engine المتخصص في التفكيك الأكاديمي الهندسي الصارم وتبسيط المفاهيم بأسلوب فاينمان (Feynman Technique).

        قم بتحليل الشريحة المرفقة بدقة وتنظيم الإجابة لتشمل قسمين أساسيين:

        📍 **القسم الأول: التحليل الأكاديمي والدراسة العلمية الرسمية**
        1. قراءة كافة النصوص والمعادلات المكتوبة بالصورة بدقة (OCR دقيق).
        2. استخراج القوانين، الرموز، والوحدات الفيزيائية والهندسية.
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

        # 5. استخدام نموذج Flash السريع والمعتمد
        model_name = 'gemini-3.8-flash'
        
        # محاولات متعددة لامتصاص زحام السيرفر الموقت (503)
        max_retries = 3
        for attempt in range(max_retries):
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

            except Exception as e:
                error_str = str(e)
                
                # التعامل مع خطأ الحصة اليومية (429 Resource Exhausted)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    return (
                        "⚠️ **تم تجاوز الحد الأقصى للطلبات المتاحة حالياً (429 Resource Exhausted).**\n\n"
                        "💡 **الحل:** انتظر دقيقة واحدة ثم أعد الضغط على زر التفكيك مجدداً."
                    )
                
                # التعامل مع خطأ الزحام اللحظي (503 UNAVAILABLE)
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    if attempt < max_retries - 1:
                        time.sleep(3)  # انتظار 3 ثوانٍ بين المحاولات
                        continue
                
                return f"⚠️ **خطأ في الاتصال بالنموذج `{model_name}`:**\n`{error_str}`"

        return "⚠️ **خوادم Google تعاني من زحام موقت (503). يرجى إعادة الضغط على زر التفكيك بعد بضع ثوانٍ.**"

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع:** `{str(general_error)}`"
