# -*- coding: utf-8 -*-
"""
لعبة 1: مشغّل غرفة التحكم في التوربينة الغازية (Turbine Control Room Operator)
=============================================================================
لعبة محاكاة تفاعلية:
- أنت مهندس التشغيل في محطة كهرباء شط البصرة.
- هدفك إكمال نوبة عمل (Shift) من 5 جولات.
- في كل جولة، تطلب شبكة الكهرباء الوطنية حملاً محدداً من الطاقة (MW).
- عليك موازنة صمام الوقود ونظام تبريد الهواء لتحقيق الطلب دون تجاوز درجات الحرارة أو الاهتزازات القصوى.
"""

import sys
import time
import random

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

def clear_screen():
    print("\n" + "=" * 65 + "\n")

def print_gauge(label, value, unit, min_val, max_val, safe_max, width=20):
    """رسم مؤشر بياني شريطي للقيم الهندسية"""
    ratio = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    status = "✅ آمن" if value <= safe_max else "⚠️ خطر!"
    print(f"  {label:<18}: [{bar}] {value:6.1f} {unit:<6} ({status})")

def play_control_room_game():
    clear_screen()
    print("      🏭 مرحباً بك في محاكي غرفة التحكم - محطة كهرباء التوربينات الغازية 🏭")
    print("=" * 65)
    print("التعليمات الهندسية:")
    print("1. شبكة الكهرباء تطلب ميجاواط (MW) متغيرة في كل جولة.")
    print("2. زيادة صمام الوقود ترفع الطاقة ولكن ترفع حرارة العادم (EGT).")
    print("3. إذا تجاوزت الحرارة 650°C أو الاهتزازات 9.0 mm/s يحدث إيقاف طارئ (TRIP) وتخسر!")
    print("4. يمكنك تشغيل رذاذ تبريد هواء السحب (Fogging) لتبريد التوربينة في الصيف.")
    print("=" * 65)
    
    input("اضغط Enter لبدء نوبة العمل...")

    # حالة التوربينة المبدئية
    fuel_valve = 50.0       # نسبة فتح صمام الوقود %
    fogging_cooling = False # نظام تبريد الهواء
    score = 0
    total_rounds = 5

    for round_num in range(1, total_rounds + 1):
        clear_screen()
        # محاكاة ظروف الجو وطلب الشبكة
        ambient_temp = random.choice([38.0, 44.0, 49.0, 52.0, 41.0])
        grid_demand = random.choice([140.0, 165.0, 190.0, 210.0, 175.0])

        print(f"⏱️ الجولة [{round_num}/{total_rounds}] | حرارة الجو الخارجي: {ambient_temp}°C | طلب الشبكة المستهدف: {grid_demand:.0f} MW")
        print("-" * 65)

        # حساب المعاملات الهندسية بناءً على قرارات اللاعب
        cooling_effect = 25.0 if fogging_cooling else 0.0
        power_generated = (fuel_valve * 2.5) - (ambient_temp * 0.8) + (cooling_effect * 0.6)
        egt_temp = 420.0 + (fuel_valve * 2.6) + (ambient_temp * 0.9) - cooling_effect
        vibration = 2.0 + (fuel_valve * 0.07) + (0.05 * (ambient_temp - 35))

        # عرض عدادات التوربينة
        print("📊 لوحة العدادات الحية (SCADA Dashboard):")
        print_gauge("طاقة التوليد (MW)", power_generated, "MW", 50, 250, 260)
        print_gauge("حرارة العادم (EGT)", egt_temp, "°C", 350, 700, 640)
        print_gauge("مستوى الاهتزازات", vibration, "mm/s", 0, 12, 8.5)
        print(f"  صمام الوقود الحالي : {fuel_valve:.1f} %")
        print(f"  نظام تبريد السحب   : {'[مُفعل ❄️]' if fogging_cooling else '[مُغلق 🛑]'}")
        print("-" * 65)

        # فحص شروط الحماية والـ Trip
        if egt_temp >= 650.0:
            print("\n🚨🚨 [إيقاف اضطراري كلي - EMERGENCY TRIP] 🚨🚨")
            print(f"احترقت ريش التوربينة! تجاوزت حرارة العادم الحد الأقصى: {egt_temp:.1f}°C > 650°C")
            print("انقطعت الكهرباء عن المدينة وفشلت المهمة! ❌")
            return

        if vibration >= 9.0:
            print("\n🚨🚨 [إيقاف اضطراري للاهتزاز - VIBRATION TRIP] 🚨🚨")
            print(f"اهتزازات خطيرة في المحامل: {vibration:.1f} mm/s > 9.0 mm/s")
            print("توقف الروتور خوفاً من تدمير الغلاف الخارجي! ❌")
            return

        # حساب دقة التوليد بالنسبة للطلب
        power_diff = abs(power_generated - grid_demand)
        if power_diff <= 10.0:
            print("🌟 [أداء مثالي]: الطاقة المولدة متطابقة تماماً مع طلب الشبكة!")
            score += 20
        elif power_diff <= 25.0:
            print("👍 [أداء جيد]: استجابة مقبولة لحمل الشبكة.")
            score += 10
        else:
            print("⚠️ [عجز/فائض]: فرق كبير بين التوليد وطلب الشبكة.")

        if round_num == total_rounds:
            break

        # خيارات التحكم للاعب
        print("\n⚙️ خيارات التحكم للمهندس:")
        print(" [1] زيادة صمام الوقود (+10%)")
        print(" [2] خفض صمام الوقود (-10%)")
        print(" [3] تشغيل / إيقاف تبريد هواء السحب (Fogging Toggle)")
        print(" [4] الإبقاء على نفس الإعدادات والمتابعة")
        
        choice = input("\nأدخل رقم الإجراء (1 - 4): ").strip()
        if choice == "1":
            fuel_valve = min(100.0, fuel_valve + 10.0)
            print(">> تم رفع ضخ الوقود.")
        elif choice == "2":
            fuel_valve = max(20.0, fuel_valve - 10.0)
            print(">> تم تقليل ضخ الوقود.")
        elif choice == "3":
            fogging_cooling = not fogging_cooling
            state_str = "تشغيل" if fogging_cooling else "إيقاف"
            print(f">> تم {state_str} نظام تبريد الهواء.")
        else:
            print(">> استمرار بالوضع الحالي.")
        
        time.sleep(1)

    clear_screen()
    print("🎉 انتهت نوبة العمل بنجاح تام! 🎉")
    print(f"النتيجة النهائية للمهندس: {score} من 100 نقطة.")
    if score >= 80:
        print("🏆 رتبتك: كبير مهندسي تشغيل التوربينات (Senior Turbomachinery Chief)!")
    elif score >= 50:
        print("🎖️ رتبتك: مهندس تشغيل معتمد (Qualified Plant Operator).")
    else:
        print("📝 رتبتك: مهندس متدرب يحتاج لمزيد من الممارسة.")
    print("=" * 65)

if __name__ == "__main__":
    play_control_room_game()
