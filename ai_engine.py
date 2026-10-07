import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي والتفكيك بأسلوب فاينمان.
    مزود بنظام معالجة الأخطاء والتنقل التلقائي بين النماذج المعتمدة لضمان الاستقرار.
    """
    # 1. التحقق من وجود مفتاح API
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى إضافته في Streamlit Secrets."

    # 2. تجهيز العميل والصورة
    try:
        client = genai.Client(api_key=api_key)
        image = Image.open(image_file).convert("RGB")
    except Exception as e:
        return f"❌ **خطأ أثناء قراءة ملف الصورة:** `{str(e)}`"

    # 3. توجيهات النظام (الدقة الأكاديمية + أسلوب فاينمان)
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
    2. استخدم تشبيهات وأمثلة ملموسة من الحياة اليومية.
    3. فكك القانون الرياضي إلى معناه الفيزيائي الملموس.

    🔴 **قاعدة منع الهلوسة:** لا تضف أي بيانات غير موجودة بالصورة المرفقة.
    """

    prompt = f"قم بقراءة وتحليل هذه الشريحة الأكاديمية بالكامل بلغة: {target_language}. اربط الشرح الأكاديمي بقسم فاينمان المبسط."

    # 4. النماذج الرسمية والمستقرة مرتبة حسب الأسرع والأحدث
    candidate_models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]

    last_error_message = ""

    # 5. التنفيذ المباشر مع إعادة المحاولة والتحويل الآلي عند الضغط
    for model_name in candidate_models:
        for attempt in range(2):  # محاولتان لكل نموذج لامتصاص أي زحام لحظي
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
                last_error_message = str(e)
                # إذا كان خطأ زحام موقت (503)، ننتظر 2 ثانية ونحاول مجدداً
                if "503" in last_error_message or "UNAVAILABLE" in last_error_message or "high demand" in last_error_message:
                    time.sleep(2)
                    continue
                # لأي خطأ آخر (مثل 429)، ننتقل فوراً للنموذج التالي
                break

    return (
        "⚠️ **تعذر الاتصال بالخوادم في الوقت الحالي بسبب ضغط عالي جداً من سيرفرات Google.**\n\n"
        f"**آخر خطأ مسجل:** `{last_error_message}`\n\n"
        "💡 **الحل:** انتظر بضع ثوانٍ ثم أعد الضغط على زر التحليل."
    )
