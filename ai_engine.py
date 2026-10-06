import streamlit as st

# البرومبت الموحد بـ 10 أقسام و 12 شرطاً صارماً
SYSTEM_PROMPT_AR = """
أنت محرك تحليل أكاديمي صارم (ZINO Vision Engine). عند تحليل أي صورة أو صفحة كتاب أو مخطط علمي/هندسي مرفوع، يجب عليك التزام الأقسام الـ 10 التالية وبالتسلسل تماماً:

📚 الموضوع: [اسم الدرس/الموضوع المباشر من المصدر]
🎯 الفكرة الأساسية: [الفكرة الرئيسية كما وردت]
📖 التعريفات: [جميع المصطلحات والتعريفات المذكورة]
🧮 المعادلات: [المعادلات بصيغة LaTeX دقيقة دون تغيير]
🔤 الرموز والوحدات: [تعريف كل رمز ووحدته القياسية]
⚙️ شروط استخدام القوانين: [حدود وشروط تطبيق كل قانون]
📝 الأمثلة والحلول: [الأمثلة والتمارين المحلولة إن وجدت]
💡 شرح مبسط: [توضيح مبسط ومستقل ومفصول عن النص الأصلي]
📌 أهم النقاط للحفظ: [نقاط ملخصة ومباشرة]
📄 مصدر كل معلومة: [تحديد رقم الصفحة/القسم أو المخطط]

⚠️ القواعد والتعليمات الصارمة (12 شرطاً):
1. لا تخترع أي معلومة.
2. لا تغير أي معادلة.
3. لا تحذف شرطاً مهمأ للقانون.
4. عرّف جميع الرموز المهمة.
5. حافظ على الوحدات.
6. اربط كل معلومة بمصدرها/صفحتها.
7. إذا كانت المعلومة غير واضحة، قل إنها غير واضحة ولا تخمن.
8. افصل بين محتوى المصدر والشرح الإضافي.
9. لا تضف معرفة خارجية إلا إذا طلب المستخدم ذلك.
10. أعطِ الأولوية للدقة العلمية على الأسلوب الجميل.
11. حافظ على ترتيب وتسلسل المحاضرة/الدرس.
12. تحقق من المعادلات قبل عرضها.
"""

SYSTEM_PROMPT_EN = """
You are a rigorous academic analysis engine (ZINO Vision Engine). Analyze the uploaded page/diagram following these 10 exact sections and 12 strict rules:

📚 Subject / Topic
🎯 Core Idea
📖 Definitions
🧮 Equations (LaTeX)
🔤 Symbols & Units
⚙️ Conditions for Using Laws
📝 Examples & Solutions
💡 Simplified Explanation (Separated from primary text)
📌 Key Points to Memorize
📄 Source of Each Information

⚠️ Strict Rules:
1. Do not invent any information.
2. Do not alter any equation.
3. Do not drop any law usage conditions.
4. Define all important symbols.
5. Preserve units.
6. Link info to source/page.
7. If unclear, state it explicitly without guessing.
8. Separate source content from extra explanations.
9. Do not add outside knowledge unless requested.
10. Prioritize scientific accuracy over aesthetics.
11. Preserve lecture sequence.
12. Verify equations before displaying.
"""

SYSTEM_PROMPT_RU = """
Вы — академический аналитический движок (ZINO Vision Engine). Проанализируйте загруженный документ по 10 разделам и 12 строгим правилам:

📚 Тема
🎯 Основная идея
📖 Определения
🧮 Уравнения (LaTeX)
🔤 Символы и единицы измерения
⚙️ Условия применения законов
📝 Примеры и решения
💡 Упрощенное объяснение
📌 Ключевые моменты для запоминания
📄 Источник информации

⚠️️ Строгие правила:
1. Не выдумывайте информацию.
2. Не меняйте уравнения.
3. Сохраняйте все условия законов.
4. Определяйте все символы.
5. Сохраняйте единицы измерения.
6. Указывайте источник/страницу.
7. Не угадывайте неясные данные.
8. Разделяйте текст источника и пояснения.
9. Не добавляйте внешних знаний.
10. Приоритет — научная точность.
11. Сохраняйте порядок лекции.
12. Проверяйте формулы перед выводом.
"""

def get_system_prompt(language):
    if language == "Arabic":
        return SYSTEM_PROMPT_AR
    elif language == "Russian":
        return SYSTEM_PROMPT_RU
    return SYSTEM_PROMPT_EN

def process_stem_analysis(image_file, target_lang):
    """
    دالة معالجة وتحليل الصور المرفوعة وفق الأقسام الـ 10 والشروط الـ 12
    """
    prompt = get_system_prompt(target_lang)
    
    # مخرجات هيكلية نموذجية لربطها بالنموذج المختار (Gemini Vision API / OpenCV Pipeline)
    if target_lang == "Arabic":
        return """
📚 **الموضوع:** الديناميكا الحرارية والقانون الأول (Thermodynamics)

🎯 **الفكرة الأساسية:** دراسة تحول الطاقة الحرارية إلى شغل ميكانيكي والتغير في الطاقة الداخلية للنظام المغلق.

📖 **التعريفات:**
- **الطاقة الداخلية ($U$):** مجموع الطاقات الميكروية لكافة جزيئات النظام.
- **الشغل ($W$):** الطاقة المنقولة عبر حدود النظام نتيجة تأثير قوة لمسافة معينة.

🧮 **المعادلات:**
$$\Delta U = Q - W$$
$$W = \int_{V_1}^{V_2} P \, dV$$

🔤 **الرموز والوحدات:**
- $\Delta U$: التغير في الطاقة الداخلية — الجول ($\text{J}$).
- $Q$: كمية الحرارة المضافة للنظام — الجول ($\text{J}$).
- $W$: الشغل المبذول بواسطة النظام — الجول ($\text{J}$).
- $P$: الضغط — الباسكال ($\text{Pa}$).
- $V$: الحجم — المتر المكعب ($\text{m}^3$).

⚙️ **شروط استخدام القوانين:**
1. تطبق معادلة $W = \int P \, dV$ فقط في العمليات المتوازنة شبه الساكنة (Quasi-static process).
2. يكون الشغل موجب القيمة ($W > 0$) عند تمدد النظام فقط.

📝 **الأمثلة والحلول:**
- *مثال 1 (ص 42):* غاز محصور تحت ضغط ثابت قدره $100 \text{ kPa}$ تمدد من $0.01 \text{ m}^3$ إلى $0.03 \text{ m}^3$.
  $$\text{الحل: } W = P \Delta V = 100 \times 10^3 \times (0.03 - 0.01) = 2000 \text{ J} = 2 \text{ kJ}$$

💡 **شرح مبسط (خارج النص الأصلي):**
تخيل أن الطاقة الداخلية هي رصيدك في البنك؛ الشراء هو الشغل المبذول ($W$)، والإيداع هو الحرارة المضافة ($Q$).

📌 **أهم النقاط للحفظ:**
- القانون الأول هو صياغة لقانون حفظ الطاقة.
- العمليات المعزولة حرارياً تكون فيها $Q = 0$.

📄 **مصدر كل معلومة:**
- الشكل والمخطط: الصفحة 41، الشكل (3-2).
- الأمثلة والمعادلات: الصفحة 42، الفقرة الثانية.
"""
    elif target_lang == "Russian":
        return """
📚 **Тема:** Термодинамика и Первое Начало

🎯 **Основная идея:** Преобразование тепловой энергии в механическую работу и изменение внутренней энергии.

📖 **Определения:**
- **Внутренняя энергия ($U$):** Сумма микроскопических энергий всех частиц системы.

🧮 **Уравнения:**
$$\Delta U = Q - W$$

🔤 **Символы и единицы:**
- $\Delta U$: Изменение внутренней энергии — Джоуль ($\text{J}$).
- $Q$: Количество теплоты — Джоуль ($\text{J}$).
- $W$: Работа системы — Джоуль ($\text{J}$).

⚙️ **Условия применения:**
1. Формула работы применима только для квазистатических процессов.

📝 **Примеры:**
- Пример со страницы 42: $W = P \Delta V = 2000 \text{ J}$.

💡 **Упрощенное объяснение:**
Внутренняя энергия похожа на банковский счет: тепло — пополнение, работа — снятие денег.

📌 **Ключевые моменты:**
- Первое начало — закон сохранения энергии.

📄 **Источник:** Страница 41-42, раздел 3.2.
"""
    else:
        return """
📚 **Subject:** Thermodynamics & First Law

🎯 **Core Idea:** Transformation of thermal energy into mechanical work and internal energy variation.

📖 **Definitions:**
- **Internal Energy ($U$):** Microscopic energy sum of all particles in the system.

🧮 **Equations:**
$$\Delta U = Q - W$$

🔤 **Symbols & Units:**
- $\Delta U$: Internal Energy Change — Joules ($\text{J}$).
- $Q$: Heat Added — Joules ($\text{J}$).
- $W$: Work Done by System — Joules ($\text{J}$).

⚙️ **Conditions:**
1. Valid strictly for quasi-static equilibrium processes.

📝 **Examples:**
- Page 42 Example: $W = P \Delta V = 2000 \text{ J}$.

💡 **Simplified Explanation:**
Think of internal energy as a bank account balance: Heat is deposit, Work is withdrawal.

📌 **Key Points:**
- The First Law expresses conservation of energy.

📄 **Source:** Page 41-42, Section 3.2.
"""
