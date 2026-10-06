import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي الهندسي المتقدم بتأطير فاينمان.
    مزود بنظام حماية متعدد الطبقات لتفادي أخطاء ضغط الخوادم (503 High Demand).
    """
    try:
        # 1. جلب مفتاح API بأمان
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

        # 2. إنشاء عميل الذكاء الاصطناعي
        client = genai.Client(api_key=api_key)

        # 3. معالجة وتجهيز الصورة بنظام الألوان القياسي RGB
        image = Image.open(image_file).convert("RGB")

        # 4. توجيهات النظام الصارمة (الدقة الأكاديمية + أسلوب فاينمان التفاعلي)
        system_instruction = """
        أنت محرك ZINO Vision Engine المتخصص في التفكيك الأكاديمي الهندسي الصارم وتبسيط المفاهيم بأسلوب فاينمان (Feynman Technique).

        مهمتك الأساسية هي تحليل الشريحة/الصورة المرفقة بدقة وتنظيم الإجابة لتشمل قسمين أساسيين:

        📍 **القسم الأول: التحليل الأكاديمي والدراسة العلمية الرسمية**
        1. إجراء مسح بصري دقيق (OCR) وقراءة النصوص والمعادلات المكتوبة بالصورة فقط.
        2. استخراج القوانين، الرموز، والوحدات الفيزيائية والهندسية بشكل دقيق.
        3. تنسيق كافة معادلات ورموز LaTeX بعناية:
           - المعادلات المستقلة في أسطر منفصلة ضعها بين $$...$$
           - الرموز والمتغيرات المدمجة داخل النص ضعها بين $...$

        📍 **القسم الثاني: تشبيه فاينمان السلس والتفاعلي (Feynman Intuition)**
        1. اشرح المفهوم الهندسي/الفيزيائي الرئيسي بلغة بسيطة للغاية وكأنك تشرح لشخص لا يمتلك أي خلفية هندسية.
        2. استخدم تشبيهات وأمثلة ملموسة من الحياة اليومية (مثل: تشبيه المادة بنوابض ميكروسكوبية، أو تشبيه معامل يونغ E بصلابة حبل الغسيل، أو تشبيه التخصر Necking بسحب قطعة علكة أو معجون حتى تنقطع).
        3. فكك القانون الرياضي إلى معناه الفيزيائي الملموس (ماذا تفعل القوة، الطول، المساحة، ومعامل المرونة).
        4. ركز على بناء "الإدراك الفيزيائي والميكانيكي" بدلاً من مجرد نقل عناوين الشرائح.

        🔴 **قاعدة منع الهلوسة الصارمة (Zero Hallucination):**
        لا تخترع أو تضف أي أرقام أو بيانات غير موجودة في الصورة المرفقة.
        """

        prompt = f"""
        قم بقراءة وتحليل هذه الشريحة الأكاديمية المرفقة بالكامل بلغة: {target_language}.
        اربط الشرح الأكاديمي الدقيق بقسم فاينمان المبسط والمدعوم بالتشبيهات والأمثلة الملموسة.
        """

        # 5. قائمة النماذج المرشحة بالتتابع لتجاوز ضغط السيرفرات (503 High Demand)
        candidate_models = [
            'gemini-3.8-flash',
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-1.5-flash'
        ]

        last_error = None

        # 6. التنقل بين النماذج تلقائياً في حال وجود ضغط على أحدها
        for model_name in candidate_models:
            for retry in range(2): # محاولتان لكل نموذج قبل الانتقال للنموذج التالي
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
                    last_error = e
                    # انتظار تدريجي قصير قبل المحاولة التالية لتخفيف الضغط
                    time.sleep(1.5 * (retry + 1))

        return (
            "⚠️ **سيرفرات جوجل تعاني من ضغط مرتفع جداً في هذه اللحظة (503 High Demand).**\n\n"
            f"**تفاصيل الخطأ:** `{str(last_error)}`\n\n"
            "💡 **المشكلة موقتة من خوادم Google، يُرجى إعادة الضغط على زر التفكيك بعد بضع ثوانٍ.**"
        )

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع أثناء المعالجة:** `{str(general_error)}`"
