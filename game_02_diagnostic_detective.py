# -*- coding: utf-8 -*-
"""
لعبة 5: المحقق الهندسي - كاشف أعطال التوربينات (Turbomachinery Diagnostic Detective)
=================================================================================
لعبة ذكاء وتشخيص أعطال:
- أنت كبير مهندسي الصيانة والتشخيص في حقول ومحطات الطاقة.
- تواجه 3 قضايا أعطال غامضة طارئة.
- لديك ميزانية "ساعات فحص" محددة؛ يمكنك طلب فحوصات معملية (تحليل اهتزازات FFT، فحص عينات الزيت، فحص البورسكوب الداخلي، فحص انتشار الحرارة).
- هدفك كشف السبب الجذري الدقيق (Root Cause) قبل انهيار التوربينة وتدمير المحطة!
"""

import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

def clear_screen():
    print("\n" + "=" * 70 + "\n")

CASES = [
    {
        "id": 1,
        "location": "محطة غاز الرميلة - توربينة ضاغط الغاز (Gas Compressor Train)",
        "alarm": "إنذار اهتزازات جانبية عالية جداً ومفاجئة على المحمل رقم 2 بعد الإقلاع بسرعة 3000 RPM.",
        "tests": {
            "1": {
                "name": "طيف الاهتزازات الترددي (FFT Spectrum Analysis)",
                "cost": 2,
                "result": "قمة اهتزاز عملاقة وحيدة عند التردد 1X (50.0 Hz) تتناسب طردياً مع مربع سرعة الدوران. الزوايا الطورية متطابقة وثابتة."
            },
            "2": {
                "name": "تحليل عينة زيت التزييت (Lube Oil Lab Test)",
                "cost": 2,
                "result": "لزوجة الزيت طبيعية جداً، ولا توجد أي شوائب معدنية من النحاس أو الحديد. طبقة الزيت نظيفة."
            },
            "3": {
                "name": "فحص الكاميرا البصرية الداخلية (Borescope Inspection)",
                "cost": 3,
                "result": "جميع ريش الضاغط سليمة ولا يوجد انكسار، لكن لوحظ فقدان أحد أوزان الموازنة الطرفية على قرص الدوران."
            },
            "4": {
                "name": "فحص توزيع حرارة الاحتراق (Exhaust Temp Spread)",
                "cost": 2,
                "result": "توزيع حرارة العادم متجانس والفرق بين المجسات أقل من 8°C (وضع احتراق مثالي)."
            }
        },
        "options": [
            "1. دوامة الزيت الهيدروديناميكية (Oil Whirl Instability)",
            "2. انعدام الموازنة الكتلية (Rotor Mass Unbalance)",
            "3. انسداد نوزلات حواقن الوقود (Fuel Nozzle Clogging)",
            "4. عدم محاذاة عمود الدوران (Shaft Misalignment 2X)"
        ],
        "correct": "2",
        "explanation": "ظهور قمة اهتزاز مهيمنة بدقة عند التردد الأساسي 1X مع فقدان وزن الموازنة يؤكد وجود Unbalance خالص (ISO 1940)."
    },
    {
        "id": 2,
        "location": "محطة كهرباء شط البصرة - توربينة غازية 9FA (250 MW)",
        "alarm": "هبوط مفاجئ في قدرة التوليد بمقدار 18 MW مع قفزة غير مسبوقة في فرق درجات الحرارة بين مجسات العادم (Temp Spread).",
        "tests": {
            "1": {
                "name": "طيف الاهتزازات الترددي (FFT Spectrum Analysis)",
                "cost": 2,
                "result": "الاهتزازات الكلية طبيعية ومستقرة تحت 2.1 mm/s، ولا توجد ترددات رنينية شاذة."
            },
            "2": {
                "name": "تحليل عينة زيت التزييت (Lube Oil Lab Test)",
                "cost": 2,
                "result": "الزيت سليم، درجة حرارة الزيت الراجع 52°C ضمن الحدود التصميمية."
            },
            "3": {
                "name": "فحص الكاميرا البصرية الداخلية (Borescope Inspection)",
                "cost": 3,
                "result": "تآكل حراري شديد وانسداد جزئي بالكربون على فوهة الحاقن في غرفة الاحتراق رقم 7 (Can #7)."
            },
            "4": {
                "name": "فحص ضغط حجرة الاحتراق وتدفق الوقود",
                "cost": 2,
                "result": "انخفاض تدفق الغاز في الخط الفرعي رقم 7 بمقدار 40%، مما أحدث بقعة باردة موضعية في العادم."
            }
        },
        "options": [
            "1. كسر في ريش المرحلة الأولى للتوربينة (HPT Blade Fracture)",
            "2. احتكاك الروتور بالمحمل (Rotor Rubbing)",
            "3. انسداد وتفحم حاقن وقود غرفة الاحتراق (Fuel Nozzle Carbon Clogging)",
            "4. انهيار طبقة التخميد في محامل كابوني (Capone Bearing Failure)"
        ],
        "correct": "3",
        "explanation": "الـ Temp Spread المرتفع في العادم هو الدليل القاطع على عدم انتظام الاحتراق الناتج عن انسداد حاقن الغاز في Can #7."
    },
    {
        "id": 3,
        "location": "محطة الهارثة الحرارية - توربينة بخارية ذات ضغط منخفض (LP Steam Turbine)",
        "alarm": "اهتزازات تذبذبية غير مستقرة (Subharmonic) بتردد فرعي منخفض عند سرعات الدوران العالية، مع ارتفاع حرارة المحمل النحاسي.",
        "tests": {
            "1": {
                "name": "طيف الاهتزازات الترددي (FFT Spectrum Analysis)",
                "cost": 2,
                "result": "ظهور تردد غير متزامن بارز عند 0.46X (أي حوالي 23 Hz عند سرعة 50 Hz)، مصحوباً بمدار اهتزاز بيضاوي متسع."
            },
            "2": {
                "name": "تحليل عينة زيت التزييت (Lube Oil Lab Test)",
                "cost": 2,
                "result": "انخفاض حاد في لزوجة الزيت وارتفاع حرارته إلى 85°C مما قلل من قدرة إسفين الزيت الهيدروديناميكي."
            },
            "3": {
                "name": "فحص الكاميرا البصرية الداخلية (Borescope Inspection)",
                "cost": 3,
                "result": "ريش التوربينة البخارية سليمة، لكن لوحظ انزلاق طبقة التزييت في المحمل الانزلاقي."
            },
            "4": {
                "name": "فحص الفجوة الخلوصية للمحمل (Bearing Clearance Check)",
                "cost": 2,
                "result": "الخلوص الرأسي متسع فوق القيمة المسموحة مما يسمح لعمود الدوران بالطواف الحر داخل غشاء الزيت."
            }
        },
        "options": [
            "1. دوامة وتذبذب الزيت الهيدروديناميكي (Oil Whirl / Whip Instability)",
            "2. ظاهرة الطرق المائي (Water Droplet Erosion)",
            "3. انكسار ريشة الدوران الأخيرة (L-0 Blade Loss)",
            "4. تفكك براغي التثبيت الأرضية (Loose Foundation Bolts)"
        ],
        "correct": "1",
        "explanation": "التردد تحت المتزامن عند ~0.46X مع تدهور لزوجة الزيت هو التوقيع الرياضي الكلاسيكي لعدم استقرار طبقة الزيت (Oil Whirl)."
    }
]

def play_detective_game():
    clear_screen()
    print("      🕵️‍♂️ مرحباً بك في لعبة: المحقق الهندسي لكشف أعطال التوربينات 🕵️‍♂️")
    print("=" * 70)
    print("أنت المحقق الهندسي المسؤول عن حماية المحطات الاستراتيجية من الانهيار.")
    print("في كل قضية:")
    print(" - لديك ميزانية 5 ساعات استقصاء لفحص الأدلة المخبرية.")
    print(" - كل فحص يستهلك ساعات محددة؛ اختر فحوصاتك بحكمة لكشف العطل.")
    print(" - في النهاية، أصدر قرارك الهندسي لتحديد السبب الجذري!")
    print("=" * 70)
    input("اضغط Enter لتولي القضية الأولى...")

    total_score = 0

    for case in CASES:
        clear_screen()
        print(f"🚨 [البلاغ الطارئ - القضية #{case['id']}]:")
        print(f"📍 الموقع : {case['location']}")
        print(f"⚠️ الإنذار: {case['alarm']}")
        print("-" * 70)

        hours_left = 5
        seen_tests = set()

        while hours_left > 0:
            print(f"\n⏳ الساعات المتبقية في ميزانيتك: [{hours_left} ساعات]")
            print("اختر فحصاً مخبرياً لإجرائه:")
            for k, t in case["tests"].items():
                status = "[تم الفحص ✅]" if k in seen_tests else f"[يكلف {t['cost']} ساعات]"
                print(f" [{k}] {t['name']} {status}")
            print(" [D] التوجه فوراً لإصدار قرار التشخيص النهائي (Diagnose Now)")

            choice = input("\nأدخل اختيارك (1 - 4 أو D): ").strip().upper()

            if choice == "D":
                break

            if choice in case["tests"]:
                if choice in seen_tests:
                    print(">> قمت بإجراء هذا الفحص مسبقاً! اختر فحصاً آخر.")
                    continue

                test_info = case["tests"][choice]
                if test_info["cost"] > hours_left:
                    print(f">> عذراً! الفحص يتطلب {test_info['cost']} ساعات ولديك {hours_left} ساعات فقط.")
                    continue

                hours_left -= test_info["cost"]
                seen_tests.add(choice)
                print(f"\n🔬 [نتيجة الفحص المخبري - {test_info['name']}]:")
                print(f"   >> {test_info['result']}")
                time.sleep(1)
            else:
                print(">> اختيار غير صحيح.")

        # مرحلة التشخيص النهائي
        print("\n" + "=" * 70)
        print("⚖️ حان وقت إصدار القرار الهندسي الرسمي:")
        print("ما هو السبب الجذري (Root Cause) الحقيقي لهذا العطل؟")
        for opt in case["options"]:
            print(f"   {opt}")

        final_verdict = input("\nأدخل رقم إجابتك (1 - 4): ").strip()

        if final_verdict == case["correct"]:
            print("\n🎯 إجابة صحيحة وعبقرية! تم إنقاذ المحطة بنجاح! 🌟 (+35 نقطة)")
            print(f"💡 التفسير الهندسي: {case['explanation']}")
            total_score += 35
        else:
            print("\n❌ تشخيص خاطئ للأسف! كلف المحطة توقفاً وتلفاً كبيراً!")
            print(f"💡 السبب الحقيقي الصحيح كان الخيار ({case['correct']}): {case['explanation']}")

        time.sleep(2)
        if case["id"] < len(CASES):
            input("\nاضغط Enter للانتقال إلى القضية التالية...")

    clear_screen()
    print("📊 التقرير النهائي للمحقق الهندسي:")
    print(f"مجموع درجاتك: {total_score} من 105 نقطة.")
    if total_score >= 100:
        print("🏆 رتبتك: أستاذ التشخيص والاهتزازات العالمي (Master Diagnostician)! عبقري في هندسة التوربينات.")
    elif total_score >= 70:
        print("🎖️ رتبتك: كبير مهندسي صيانة موثوق (Senior Maintenance Specialist).")
    else:
        print("📚 تحتاج لمراجعة كراسة الاهتزازات وتحليل الزيوت مجدداً.")
    print("=" * 70)

if __name__ == "__main__":
    play_detective_game()
