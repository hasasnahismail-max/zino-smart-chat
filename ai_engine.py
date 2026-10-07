import os
import time
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine للتحليل الأكاديمي وتفكيك المفاهيم بأسلوب فاينمان.
    مبني على حزمة google-genai الحديثة مع معالجة صارمة للضغط ومنع أخطاء NOT_FOUND (404).
    """
    # 1. جلب مفتاح API من Streamlit Secrets أو متغيرات البيئة
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى التأكد من ضبطه في Streamlit Secrets."

    # 2. قراءة وتجهيز الصورة
    try:
        client = genai.Client(api_key=api_key)
        image = Image.open(image_file).convert("RGB")
    except Exception as e:
        return f"❌ **خطأ أثناء فتح الصورة:** `{str(e)}`"

    # 3. تعليمات النظام (الدقة الأكاديمية + أسلوب فاينمان)
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

    # 4. النماذج الحديثة والمدعومة رسمياً فقط (تم إزالة gemini-1.5 و gemini-2.0 نهائياً لمنع خطأ 404)
    candidate_models = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite"
    ]

    last_error_details = ""

    # 5. الاتصال وإعادة المحاولة مع التبديل الذكي عند الضغط
    for model_name in candidate_models:
        for attempt in range(3):  # 3 محاولات لكل نموذج لامتصاص زحام الخوادم
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

            except APIError as e:
                last_error_details = f"[{model_name}] Code {e.code}: {e.message}"
                # أخطاء الضغط المؤقت واستنفاد الحصة (503, 429, 502, 504)
                if e.code in [503, 429, 502, 504] or "UNAVAILABLE" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(2 * (attempt + 1))  # انتظار تصاعدي 2s, 4s, 6s
                    continue
                else:
                    # إذا كان الخطأ غير متعلق بالضغط، انتقل فوراً للنموذج الموالي
                    break
            except Exception as ex:
                last_error_details = f"[{model_name}] {str(ex)}"
                break

    return (
        "⚠️ **تعذر الاتصال بالخوادم حالياً بسبب ضغط مرتفع على خوادم Google.**\n\n"
        f"**التفاصيل التقنية:** `{last_error_details}`\n\n"
        "💡 **الحل:** يرجى الانتظار بضع ثوانٍ ثم الضغط على زر التحليل مجدداً."
    )
