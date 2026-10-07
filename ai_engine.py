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
    محدث مع أسماء النماذج المعتمدة رسمياً ومعالجة ذكية لأخطاء 404 والضغط.
    """
    # 1. جلب مفتاح API
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ **تنبيه:** لم يتم العثور على مفتاح API (`GEMINI_API_KEY`). يرجى التأكد من ضبطه في Streamlit Secrets."

    # 2. قراءة الصورة
    try:
        client = genai.Client(api_key=api_key)
        image = Image.open(image_file).convert("RGB")
    except Exception as e:
        return f"❌ **خطأ أثناء فتح الصورة:** `{str(e)}`"

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

    # 4. النماذج الحديثة والمعتمدة رسمياً حالياً من Google
    candidate_models = [
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-2.5-flash"
    ]

    last_error_details = ""

    # 5. الاتصال والتنقل بين النماذج
    for model_name in candidate_models:
        for attempt in range(2):
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
                
                # إذا كان النموذج غير موجود (404)، انتقل للنموذج التالي فوراً
                if e.code == 404 or "404" in str(e):
                    break
                
                # أخطاء الضغط المؤقت (503 / 429)، انتظر ثانيتين وأعد المحاولة
                if e.code in [503, 429, 502, 504] or "UNAVAILABLE" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(2)
                    continue
                else:
                    break
            except Exception as ex:
                last_error_details = f"[{model_name}] {str(ex)}"
                break

    return (
        "⚠️ **تعذر الاتصال بالخوادم حالياً بسبب ضغط مرتفع على خوادم Google.**\n\n"
        f"**التفاصيل التقنية:** `{last_error_details}`\n\n"
        "💡 **الحل:** يرجى الانتظار بضع ثوانٍ ثم الضغط على زر التحليل مجدداً."
    )
