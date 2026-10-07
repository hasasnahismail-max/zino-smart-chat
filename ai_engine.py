import os
import time
from PIL import Image
from google import genai
from google.genai.errors import APIError

def analyze_image_with_gemini(image: Image.Image, prompt: str) -> str:
    """
    تحليل الصور باستخدام نماذج Gemini 2.5 الحديثة والمدعومة فقط،
    مع التعامل مع أخطاء الضغط وإعادة المحاولة تلقائياً.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "❌ خطأ: لم يتم العثور على مفتاح API. يرجى التأكد من ضبط GEMINI_API_KEY."

    client = genai.Client(api_key=api_key)

    # النماذج الحديثة والمدعومة رسمياً فقط (تم استبعاد gemini-1.5 المتقادم)
    candidate_models = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite"
    ]

    last_exception = None

    for model_name in candidate_models:
        # محاولة كل نموذج حتى 3 مرات عند وجود ضغط على السيرفر (503 / 429)
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[image, prompt]
                )
                if response and response.text:
                    return response.text
            except APIError as e:
                last_exception = e
                # في حال كان الخطأ بسبب الضغط (503) أو تجاوز حد الطلبات (429)
                if e.code in [503, 429, 502, 504]:
                    time.sleep(2 * (attempt + 1))  # انتظار ثانيتين ثم أربع ثوانٍ...
                    continue
                else:
                    # إذا كان الخطأ غير متعلق بالضغط (مثل 404)، انتقل للنموذج التالي مباشرة
                    break
            except Exception as e:
                last_exception = e
                break

    return f"⚠️ تعذر الاتصال بالخوادم حالياً بعد عدة محاولات.\nتفاصيل الخطأ: {last_exception}"
