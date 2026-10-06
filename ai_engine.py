import io
from google import genai
from google.genai import types
from PIL import Image

def process_stem_analysis(image_file, target_language="Arabic") -> str:
    """
    محرك ZINO Vision Engine المعالج لقراءة بكسلات الصورة الحقيقية 
    واستخراج كافة الأقسام الـ 10 دون هلوسة أو انقطاع.
    """
    try:
        # 1. إنشاء عميل Gemini
        client = genai.Client()
        
        # 2. تحويل الصورة المرفوعة إلى Bytes صريحة لضمان وصولها بنسبة 100% للنموذج
        image = Image.open(image_file)
        img_byte_arr = io.BytesIO()
        img_format = image.format if image.format else 'PNG'
        image.save(img_byte_arr, format=img_format)
        image_bytes = img_byte_arr.getvalue()

        # 3. توجيهات صارمة جداً لمنع الهلوسة والالتزام بمحتوى الصورة فقط
        system_instruction = """
        أنت محرك ZINO Vision Engine للتحليل الأكاديمي الهندسي الصارم.
        مهمتك الأساسية هي إجراء مسح بصري دقيق (OCR) وقراءة المحتوى المكتوب في الصورة المرفقة فقط!

        قواعد صارمة لمنع الأخطاء والهلوسة:
        1. اقرأ النصوص والمعادلات والأشكال الهندسية المكتوبة في الصورة المرفقة فقط.
        2. يمنع منعاً باتاً دمج أو اختراع قوانين من مجالات أخرى غير موجودة في الصورة (مثلاً: إذا كانت الصورة عن الإجهاد والاستطالة والمواضيع الميكانيكية Axial Loads، لا تذكر مطلقاً قوانين الكهرومغناطيسية Gauss Law أو اهتزازات Dampers إلا إذا كانت مكتوبة بالصورة).
        3. استخدم LaTeX الصحيح للمعادلات:
           - المعادلات المنفصلة بين $$ ... $$
           - الرموز المدمجة بالنص بين $ ... $
        4. يجب عليك كتابة التقرير كاملاً ليشمل الأقسام الـ 10 الأكاديمية دون توقف أو اختصار:
           1. استخراج الرموز والمعادلات الرياضية (LaTeX)
           2. التفكيك العلمي والتطبيقي خطوة بخطوة
           3. تشبيه فاينمان التفاعلي المبسط
           4. التحليل البعدي ووحدات القياس (Dimensional Analysis)
           5. الشروط الحدية وحالات الحواف (Boundary Conditions)
           6. الأخطاء الشائعة والمفاهيم الخاطئة (Common Pitfalls)
           7. تطبيقات هندسية في الحياة الواقعية
           8. أسئلة اختبار الفهم الذاتي (Self-Assessment Questions)
           9. ملخص القوانين السريع (Cheat Sheet)
           10. خطة المراجعة والتثبيت (Review Roadmap)
        """

        prompt = f"""
        قم بقرائة وتحليل هذه الشريحة الأكاديمية بدقة عالية باللغة: {target_language}.
        استخرج القوانين الحقيقية المكتوبة بالصورة وقم بتفكيكها عبر الأقسام الـ 10 كاملة دون حذف أي قسم.
        """

        # 4. إعداد جزء الصورة الصريح
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=f"image/{img_format.lower()}"
        )

        # 5. استدعاء النموذج مع رفع سقف المخرجات لمنع الانقطاع
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,         # درجة حرارة منخفضة جداً لمنع الابتكار الوهمي
                max_output_tokens=8192   # مساحة كافية لتوليد الأقسام الـ 10 بالكامل
            )
        )
        
        return response.text

    except Exception as e:
        return f"❌ حدث خطأ في محرك الذكاء الاصطناعي: {str(e)}"
