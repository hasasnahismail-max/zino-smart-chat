import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي وتفكيك المفاهيم بأسلوب فاينمان (Feynman Technique).
    مربوط بأحدث إصدار من مكتبة Google GenAI ومصمم لتفادي أخطاء الضغط (503) والنماذج المفقودة (404).
    """
    try:
        # 1. التحقق من وجود مفتاح الـ API
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى التأكد من إضافته في Streamlit Secrets."

        # 2. إنشاء عميل SDK الخاص بـ Google GenAI
        client = genai.Client(api_key=api_key)

        # 3. تجهيز وتحويل الصورة إلى نظام RGB
        image = Image.open(image_file).convert("RGB")

        # 4. توجيهات النظام الصارمة (تفكيك أكاديمي دقيق + أسلوب فاينمان التفاعلي)
        system_instruction = """
        أنت محرك ZINO Vision Engine المتخصص في التفكيك الأكاديمي الهندسي الصارم وتبسيط المفاهيم بأسلوب فاينمان (Feynman Technique).

        قم بتحليل الشريحة المرفقة بدقة وتنظيم الإجابة لتشمل قسمين أساسيين:

        📍 **القسم الأول: التحليل الأكاديمي والدراسة العلمية الرسمية**
        1. قراءة كافة النصوص والمعادلات المكتوبة بالصورة بدقة (OCR دقيق).
        2. استخراج القوانين، الرموز، والوحدات الفيزيائية والهندسية المذكورة فقط.
        3. تنسيق كافة معادلات ورموز LaTeX بعناية:
           - المعادلات المستقلة في أسطر منفصلة ضعها بين $$...$$
           - الرموز والمتغيرات المدمجة داخل النص ضعها بين $...$

        📍 **القسم الثاني: تشبيه فاينمان السلس والتفاعلي (Feynman Intuition)**
        1. اشرح المفهوم الهندسي/الفيزيائي الرئيسي بلغة بسيطة جداً وكأنك تشرح لشخص ليس لديه خلفية هندسية.
        2. استخدم تشبيهات وأمثلة ملموسة من الحياة اليومية (مثل: تشبيه المادة بنوابض ميكروسكوبية، تشبيه معامل يونغ E بصلابة حبل الغسيل، أو تشبيه التخصر Necking بسحب قطعة علكة أو معجون حتى تنقطع).
        3. فكك القانون الرياضي إلى معناه الفيزيائي الملموس:
           - ماذا تفعل القوة P؟
           - ما دور الطول L؟
           - ما دور المساحة A ومعامل المرونة E في المقاومة؟
        4. ركز على بناء الإدراك الفيزيائي والميكانيكي الحقيقي.

        🔴 **قاعدة منع الهلوسة الصارمة:** لا تخترع أو تضف أي بيانات أو أرقام غير موجودة في الصورة المرفقة.
        """

        prompt = f"قم بقراءة وتحليل هذه الشريحة الأكاديمية بالكامل بلغة: {target_language}. اربط الشرح الأكاديمي الدقيق بقسم فاينمان المبسط."

        # 5. قائمة النماذج القياسية المستقرة من جوجل
        # استخدام gemini-2.5-flash كنموذج رئيسي ثابت وسريع لتجنب الـ 503 والـ 404
        models_to_try = ['gemini-2.5-flash', 'gemini-2.5-pro']
        
        last_error = ""

        for model_name in models_to_try:
            for attempt in range(2): # محاولتان سريعتان لكل نموذج
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
                    last_error = str(e)
                    # إذا كان الخطأ بسبب ضغط مؤقت (503)، ننتظر ثانيتين ونحاول مجدداً
                    if "503" in last_error or "UNAVAILABLE" in last_error:
                        time.sleep(2)
                        continue
                    # إذا كان الخطأ غير ذلك، ننتقل فوراً للنموذج التالي في القائمة
                    break

        return f"⚠️ **تعذر الاتصال بمركز معالجة Google حالياً.**\n\n**تفاصيل الخطأ:** `{last_error}`\n\n💡 **يرجى إعادة الضغط على الزر مرة أخرى.**"

    except Exception as general_error:
        return f"❌ **حدث خطأ غير متوقع أثناء المعالجة:** `{str(general_error)}`"
