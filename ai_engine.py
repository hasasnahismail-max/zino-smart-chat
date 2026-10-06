import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine المطور للتحليل الأكاديمي الشامل وتفكيك المفاهيم بأسلوب فاينمان المبسط.
    يحتوي على آلية معالجة الأخطاء وإعادة المحاولة التلقائية (Auto-Retry) لاستقرار الخدمة.
    """
    try:
        # 1. جلب مفتاح API بأمان من Secrets أو بيئة العمل
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

        # 2. تهيئة عميل Google GenAI SDK الحديث
        client = genai.Client(api_key=api_key)

        # 3. معالجة وتجهيز الصورة بنظام الألوان القياسي RGB
        image = Image.open(image_file).convert("RGB")

        # 4. توجيهات النظام الصارمة (تدمج الدقة الأكاديمية مع أسلوب فاينمان التفاعلي)
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
        3. فكك القانون الرياضي (مثل ΔL = (P * L) / (A * E)) إلى معناه الفيزيائي الملموس:
           - ماذا تفعل القوة P؟ (تسحب وتمدد)
           - ما دور الطول L؟ (يزيد من الفرصة والمدى للتمدد)
           - ما دور المساحة A والمعامل E؟ (يمثلان حائط الصد والمقاومة ضد التمدد)
        4. ركز على بناء "الإدراك الفيزيائي والميكانيكي" بدلاً من مجرد نقل عناوين الشرائح.

        🔴 **قاعدة منع الهلوسة الصارمة (Zero Hallucination):**
        لا تخترع أو تضف أي أرقام أو بيانات غير موجودة في الصورة المرفقة.
        """

        prompt = f"""
        قم بقراءة وتحليل هذه الشريحة الأكاديمية المرفقة بالكامل بلغة: {target_language}.
        اربط الشرح الأكاديمي الدقيق بقسم فاينمان المبسط والمدعوم بالتشبيهات والأمثلة الملموسة.
        """

        # 5. النموذج المعتمد رسمياً ونظام إعادة المحاولة للتغلب على ضغط السيرفر (503)
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
                        temperature=0.2
                    )
                )
                
                if response and response.text:
                    return response.text
                    
            except Exception as e:
                last_error = e
                time.sleep(2)  # انتظار ثانيتين قبل إعادة المحاولة تلقائياً

        return (
            "⚠️ **السيرفر يعاني من ضغط مؤقت.**\n"
            f"تفاصيل الخطأ: `{str(last_error)}`\n\n"
            "💡 **حل:** اضغط على زر التفكيك مرة أخرى بعد 3 ثوانٍ."
        )

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع أثناء المعالجة:** `{str(general_error)}`"
