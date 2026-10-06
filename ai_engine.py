import os
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    يقوم بتحليل مادة STEM من الصورة واستخراج الأقسام الـ 10 الصارمة والشروط الـ 12
    مع الالتزام التام بالمعادلات الموجودة في الصورة فقط ومنع الهلوسة.
    """
    try:
        # 1. إعداد العميل (تأكد من ضبط متغير البيئة GEMINI_API_KEY)
        client = genai.Client()
        
        # 2. فتح الصورة
        img = Image.open(image_file)

        # 3. صياغة البرومبت الهيكلي الصارم
        system_instruction = """
        أنت محرك تحليل أكاديمي صارم (ZINO Vision Engine) متخصص في مواد STEM (الهندسة والفيزياء والرياضيات).
        
        قواعد صارمة جداً لمنع الأخطاء:
        1. استخرج فقط المعادلة والرموز المكتوبة فعلياً في الصورة المرفوقة! يمنع منعاً باتاً اختراع قوانين من مجالات أخرى (مثلاً لا تخلط الكهرومغناطيسية أو الاهتزازات إذا كانت الصفحة عن مقاومة المواد والأحمال المحورية).
        2. استخدم تنسيق LaTeX الصحيح للمعادلات:
           - للمعادلات المنفصلة ضعها داخل $$ ... $$
           - للرموز داخل السطر ضعها داخل $ ... $
        3. اكتب جميع الأقسام الـ 10 الأكاديمية كاملة دون حذف أي قسم:
           - القسم 1: استخراج الرموز والمعادلات الرياضية (LaTeX)
           - القسم 2: التفكيك العلمي والتطبيقي خطوة بخطوة
           - القسم 3: تشبيه فاينمان التفاعلي المبسط
           - القسم 4: التحليل البعدي ووحدات القياس (Dimensional Analysis)
           - القسم 5: الشروط الحدية وحالات الحواف (Boundary Conditions)
           - القسم 6: الأخطاء الشائعة والمفاهيم الخاطئة (Common Pitfalls)
           - القسم 7: تطبيقات هندسية في الحياة الواقعية
           - القسم 8: أسئلة اختبار الفهم الذاتي (Self-Assessment Questions)
           - القسم 9: ملخص القوانين السريع (Cheat Sheet)
           - القسم 10: خطة المراجعة والتثبيت (Review Roadmap)
        """

        prompt = f"""
        قم بتحليل هذه الصفحة الأكاديمية بالكامل باللغة: {target_language}.
        
        تأكد من قراءة كل نص وشكل هندسي ومعادلة في الصورة بدقة متناهية، ثم خرج التقرير الأكاديمي الشامل المكون من الأقسام الـ 10 كاملة.
        """

        # 4. استدعاء النموذج (Gemini 2.5 Flash للرؤية السريعة والدقيقة)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1 # نسبة ابتكار منخفضة جداً لمنع الهلوسة والأخطاء Scientific Accuracy
            )
        )
        
        return response.text

    except Exception as e:
        return f"❌ حدث خطأ أثناء التحليل: {str(e)}"
