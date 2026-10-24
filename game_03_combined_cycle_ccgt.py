# -*- coding: utf-8 -*-
"""
لعبة 9: مهندس محطة الدورة المركبة الكبرى (Combined Cycle CCGT Master)
====================================================================
لعبة محاكاة وتحسين ديناميكا حرارية (Thermodynamics Optimization Game):
- أنت رئيس مهندسي التصميم لمحطة توليد طاقة هجينة تعمل بالدورة المركبة (CCGT):
  (توربينة غازية + مرجل استعادة الحرارة HRSG + توربينة بخارية).
- مهمتك موازنة البارامترات الهندسية (نسبة الانضغاط، حرارة الاحتراق، ضغط البخار، وتبريد المكثف).
- التحدي: كسر حاجز كفاءة الـ 60% العالمية وتحقيق أعلى أرباح تجارية دون إتلاف أنابيب المرجل!
"""

import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

def clear_screen():
    print("\n" + "=" * 70 + "\n")

def simulate_ccgt(pressure_ratio, firing_temp, steam_pressure, duct_firing, ambient_temp=30.0):
    """
    نموذج حراري مبسط لمحاكاة دورة برايتون الغازية مع دورة رانكن البخارية
    """
    # 1. التوربينة الغازية (Brayton Cycle)
    # كفاءة الضاغط والتوربينة الأيزنتروبية
    gamma = 1.4
    t_ambient_k = ambient_temp + 273.15
    t_comp_out_k = t_ambient_k * (pressure_ratio ** ((gamma - 1) / gamma))
    
    t_fire_k = firing_temp + 273.15
    t_exhaust_k = t_fire_k / (pressure_ratio ** ((gamma - 1) / (gamma * 1.05)))
    t_exhaust_c = t_exhaust_k - 273.15

    # حرارة الوقود المدخلة
    q_fuel_mw = (t_fire_k - t_comp_out_k) * 0.45
    gt_power_mw = q_fuel_mw * (1.0 - (t_ambient_k / t_comp_out_k) * 0.92)
    gt_power_mw = max(100.0, min(350.0, gt_power_mw))
    gt_efficiency = (gt_power_mw / q_fuel_mw) * 100.0

    # 2. مرجل استعادة الحرارة والتوربينة البخارية (Rankine Cycle)
    heat_in_exhaust_mw = q_fuel_mw - gt_power_mw
    hrs_g_effectiveness = 0.82
    
    extra_duct_fuel = 40.0 if duct_firing else 0.0
    steam_heat_mw = (heat_in_exhaust_mw * hrs_g_effectiveness) + (extra_duct_fuel * 0.90)

    # كفاءة التوربينة البخارية معتمدة على ضغط البخار (كارنو معدلة)
    steam_cycle_eff = 0.32 + (steam_pressure / 150.0) * 0.08
    st_power_mw = steam_heat_mw * steam_cycle_eff

    # 3. النتائج المجمعة للدورة المركبة
    total_fuel_mw = q_fuel_mw + extra_duct_fuel
    total_power_mw = gt_power_mw + st_power_mw
    ccgt_efficiency = (total_power_mw / total_fuel_mw) * 100.0

    # حساب الجدوى الاقتصادية (دولار / ساعة)
    # سعر بيع الكهرباء = 55 دولار لكل MWh، تكلفة الغاز = 5 دولار لكل مليون وحدة حرارية (حوالي 17 دولار لكل MW حراري)
    revenue_per_hour = total_power_mw * 55.0
    cost_per_hour = total_fuel_mw * 16.5
    profit_per_hour = revenue_per_hour - cost_per_hour

    return {
        "gt_power": gt_power_mw,
        "st_power": st_power_mw,
        "total_power": total_power_mw,
        "exhaust_temp": t_exhaust_c,
        "gt_eff": gt_efficiency,
        "ccgt_eff": ccgt_efficiency,
        "profit": profit_per_hour
    }

def play_ccgt_game():
    clear_screen()
    print("      ⚡ مرحباً بك في لعبة: مهندس الدورة المركبة الكبرى (CCGT Master) ⚡")
    print("=" * 70)
    print("الهدف الهندسي:")
    print("تصميم وضبط محطة طاقة هجينة فائقة الكفاءة مكونة من:")
    print(" 1. توربينة غازية رئيسية (Gas Turbine)")
    print(" 2. مرجل استعادة الطاقة الحرارية من العادم (HRSG)")
    print(" 3. توربينة بخارية ثانوية (Steam Turbine)")
    print("\n🎯 التحدي: هل تستطيع كسر حاجز كفاءة الـ 60% وتحقيق أرباح تتجاوز 14,000 $/ساعة؟")
    print("=" * 70)
    input("اضغط Enter لبدء لوحة هندسة المحطة...")

    # القيم المبدئية
    rp = 16.0          # نسبة الانضغاط (12 - 24)
    firing_t = 1250.0  # حرارة الاحتراق (°C) (1100 - 1450)
    p_steam = 80.0     # ضغط البخار (bar) (40 - 140)
    duct_fire = False  # الحرق الإضافي في المرجل

    attempts = 5
    best_eff = 0.0

    for i in range(1, attempts + 1):
        clear_screen()
        print(f"📊 [جولة الاختبار والتوليف الهندسية: {i} من {attempts}]")
        print("-" * 70)
        print("الإعدادات التصميمية الحالية:")
        print(f" 1. نسبة انضغاط الضاغط (Pressure Ratio rp)   : {rp:.1f}")
        print(f" 2. حرارة مدخل التوربينة (Firing Temp TIT)  : {firing_t:.0f} °C")
        print(f" 3. ضغط بخار مرجل الـ HRSG (Steam Pressure) : {p_steam:.0f} bar")
        print(f" 4. الحرق الإضافي بالقناة (Duct Firing)     : {'[مُفعل 🔥]' if duct_fire else '[مُغلق ❌]'}")
        print("-" * 70)

        # تشغيل المحاكاة
        res = simulate_ccgt(rp, firing_t, p_steam, duct_fire)

        print("\n📈 [النتائج التشغيلية الصادرة من المحطة]:")
        print(f"  ⚡ طاقة التوربينة الغازية   : {res['gt_power']:6.1f} MW (كفاءة الغاز: {res['gt_eff']:.1f}%)")
        print(f"  💨 حرارة العادم الداخل للمرجل: {res['exhaust_temp']:6.1f} °C")
        print(f"  ⚡ طاقة التوربينة البخارية : {res['st_power']:6.1f} MW (طاقة إضافية مجانية من العادم!)")
        print(f"  🔥 إجمالي التوليد الكهربائي : {res['total_power']:6.1f} MW")
        print(f"  🌟 الكفاءة الحرارية المجمعة : {res['ccgt_eff']:6.2f} %")
        print(f"  💰 الأرباح التشغيلية الصافية : {res['profit']:6.0f} $/ساعة")
        print("-" * 70)

        if res["ccgt_eff"] > best_eff:
            best_eff = res["ccgt_eff"]

        # التقييم اللحظي
        if res["ccgt_eff"] >= 60.0:
            print("🏆 إنجاز عالمي مذهل! كسرت حاجز الـ 60% كفاءة وأصبحت المحطة من أرقى محطات العالم!")
        elif res["ccgt_eff"] >= 56.0:
            print("👍 كفاءة ممتازة جداً وضمن معايير المحطات الحديثة المتقدمة.")
        else:
            print("ℹ️ كفاءة جيدة، ولكن لا يزال بإمكانك استخلاص طاقة أعلى من عادم التوربينة.")

        if i == attempts:
            break

        print("\n🛠️ خيارات المهندس لتعديل التصميم:")
        print(" [1] تعديل نسبة الانضغاط (Pressure Ratio)")
        print(" [2] تعديل حرارة الاحتراق (Firing Temperature)")
        print(" [3] تعديل ضغط البخار (Steam Pressure)")
        print(" [4] تشغيل / إطفاء الحرق الإضافي (Toggle Duct Firing)")
        print(" [Enter] الإبقاء على القيم الحالية والانتقال للمقارنة")

        sub_choice = input("\nاختر رقماً للتعديل (1 - 4): ").strip()
        if sub_choice == "1":
            val = input("أدخل نسبة الانضغاط الجديدة (بين 12 و 24): ")
            try:
                rp = max(12.0, min(24.0, float(val)))
            except ValueError:
                pass
        elif sub_choice == "2":
            val = input("أدخل حرارة الاحتراق الجديدة (بين 1100 و 1450 °C): ")
            try:
                firing_t = max(1100.0, min(1450.0, float(val)))
            except ValueError:
                pass
        elif sub_choice == "3":
            val = input("أدخل ضغط البخار الجديد (بين 40 و 140 bar): ")
            try:
                p_steam = max(40.0, min(140.0, float(val)))
            except ValueError:
                pass
        elif sub_choice == "4":
            duct_fire = not duct_fire
            print(f">> تم تغيير حالة الحرق الإضافي.")
            time.sleep(1)

    clear_screen()
    print("🎓 تقييم أداء مهندس الدورة المركبة:")
    print(f"أعلى كفاءة مجمعة حققتها: {best_eff:.2f} %")
    if best_eff >= 60.0:
        print("🌟 رتبتك: استشاري دورات الطاقة الحرارية العالمي (Chief CCGT Architect)!")
    elif best_eff >= 56.0:
        print("🎖️ رتبتك: مهندس محطات طاقة كفء (Senior Power Plant Specialist).")
    else:
        print("📖 رتبتك: باحث في الديناميكا الحرارية يحتاج لمزيد من الموازنة بين برايتون ورانكن.")
    print("=" * 70)

if __name__ == "__main__":
    play_ccgt_game()
