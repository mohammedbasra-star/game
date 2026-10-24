# -*- coding: utf-8 -*-
"""
لعبة واجهة رسومية حقيقية: مشغّل غرفة التحكم في التوربينة الغازية (SCADA GUI)
==========================================================================
واجهة رسومية أنيقة تدعم اللغة العربية بنسبة 100% بدون أي مشكلة في خطوط الترميز.
"""

import sys
import random
import tkinter as tk
from tkinter import ttk, messagebox

class TurbineControlRoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏭 محاكي غرفة التحكم في التوربينات الغازية (SCADA Dashboard)")
        self.root.geometry("740x720")
        self.root.configure(bg="#1a1d24")
        self.root.resizable(False, False)

        # حالة اللعبة
        self.round_num = 1
        self.total_rounds = 5
        self.score = 0
        self.game_over = False

        # المتغيرات الهندسية
        self.fuel_valve = 50.0        # %
        self.fogging = False          # تبريد السحب
        self.water_injection = False  # نظام حقن الماء لمكافحة الحرارة القصوى
        self.ambient_temp = 42.0      # °C
        self.grid_demand = 175.0      # MW

        self.power_generated = 160.0
        self.egt_temp = 530.0
        self.vibration = 3.2

        self.setup_ui()
        self.update_simulation()

    def setup_ui(self):
        # 1. العنوان الرئيسي
        header_frame = tk.Frame(self.root, bg="#262b36", pady=12)
        header_frame.pack(fill="x")

        lbl_title = tk.Label(
            header_frame,
            text="🏭 محطة كهرباء البصرة الكبرى - بقيادة المهندس محمد",
            font=("Segoe UI", 16, "bold"),
            fg="#00d2ff",
            bg="#262b36"
        )
        lbl_title.pack()

        # 2. شريط حالة النوبة والشبكة
        status_bar = tk.Frame(self.root, bg="#1a1d24", pady=10)
        status_bar.pack(fill="x", padx=20)

        self.lbl_round = tk.Label(
            status_bar,
            text=f"الجولة: {self.round_num}/{self.total_rounds}",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#343a40",
            padx=12,
            pady=4
        )
        self.lbl_round.pack(side="right", padx=5)

        self.lbl_ambient = tk.Label(
            status_bar,
            text=f"حرارة الجو: {self.ambient_temp:.0f}°C ☀️",
            font=("Segoe UI", 12, "bold"),
            fg="#ffb703",
            bg="#343a40",
            padx=12,
            pady=4
        )
        self.lbl_ambient.pack(side="right", padx=5)

        self.lbl_demand = tk.Label(
            status_bar,
            text=f"طلب الشبكة المستهدف: {self.grid_demand:.0f} MW ⚡",
            font=("Segoe UI", 12, "bold"),
            fg="#00f5d4",
            bg="#343a40",
            padx=12,
            pady=4
        )
        self.lbl_demand.pack(side="right", padx=5)

        self.lbl_score = tk.Label(
            status_bar,
            text="النقاط: 0",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#7209b7",
            padx=12,
            pady=4
        )
        self.lbl_score.pack(side="left", padx=5)

        # 3. لوحة العدادات (Gauges Frame)
        gauges_frame = tk.LabelFrame(
            self.root,
            text=" 📊 قراءات الحساسات اللحظية (SCADA Telemetry) ",
            font=("Segoe UI", 12, "bold"),
            fg="#00d2ff",
            bg="#21252f",
            padx=20,
            pady=15
        )
        gauges_frame.pack(fill="x", padx=20, pady=10)

        # مقياس طاقة التوليد (Power)
        self.lbl_power = tk.Label(gauges_frame, text="", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_power.pack(anchor="e")
        self.prog_power = ttk.Progressbar(gauges_frame, orient="horizontal", length=660, mode="determinate", maximum=280)
        self.prog_power.pack(pady=4)

        # مقياس حرارة العادم (EGT)
        self.lbl_egt = tk.Label(gauges_frame, text="", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_egt.pack(anchor="e")
        self.prog_egt = ttk.Progressbar(gauges_frame, orient="horizontal", length=660, mode="determinate", maximum=700)
        self.prog_egt.pack(pady=4)

        # مقياس الاهتزازات (Vibrations)
        self.lbl_vib = tk.Label(gauges_frame, text="", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_vib.pack(anchor="e")
        self.prog_vib = ttk.Progressbar(gauges_frame, orient="horizontal", length=660, mode="determinate", maximum=12)
        self.prog_vib.pack(pady=4)

        # حالة الصمام والتبريد
        indicators_frame = tk.Frame(gauges_frame, bg="#21252f", pady=8)
        indicators_frame.pack(fill="x")

        self.lbl_valve = tk.Label(indicators_frame, text="صمام الوقود: 50.0%", font=("Segoe UI", 11, "bold"), fg="#e0e1dd", bg="#2b303c", padx=10, pady=4)
        self.lbl_valve.pack(side="right", padx=6)

        self.lbl_cooling = tk.Label(indicators_frame, text="تبريد السحب: مُغلق 🛑", font=("Segoe UI", 11, "bold"), fg="#ff4d6d", bg="#2b303c", padx=10, pady=4)
        self.lbl_cooling.pack(side="right", padx=6)

        self.lbl_water = tk.Label(indicators_frame, text="حقن الماء: مُغلق 🛑", font=("Segoe UI", 11, "bold"), fg="#ff4d6d", bg="#2b303c", padx=10, pady=4)
        self.lbl_water.pack(side="right", padx=6)

        # 4. صندوق التنبيهات والأحداث الهندسية
        self.log_box = tk.Text(
            self.root,
            height=6,
            font=("Segoe UI", 10),
            bg="#0f1117",
            fg="#70e000",
            wrap="word",
            padx=10,
            pady=8
        )
        self.log_box.pack(fill="x", padx=20, pady=8)
        self.log_message("مرحباً بك في غرفة التحكم. قم بضبط صمام الوقود لتلبية طلب الميجاواط دون تجاوز الحرارة القصوى 650°C.")

        # 5. أزرار التحكم
        ctrl_frame = tk.Frame(self.root, bg="#1a1d24", pady=10)
        ctrl_frame.pack(fill="x", padx=20)

        btn_style = {"font": ("Segoe UI", 11, "bold"), "padx": 10, "pady": 8, "cursor": "hand2"}

        self.btn_fuel_up = tk.Button(ctrl_frame, text="➕ زيادة الوقود (+10%)", bg="#0077b6", fg="white", command=lambda: self.adjust_fuel(10.0), **btn_style)
        self.btn_fuel_up.pack(side="right", padx=5)

        self.btn_fuel_down = tk.Button(ctrl_frame, text="➖ تقليل الوقود (-10%)", bg="#023e8a", fg="white", command=lambda: self.adjust_fuel(-10.0), **btn_style)
        self.btn_fuel_down.pack(side="right", padx=5)

        self.btn_fogging = tk.Button(ctrl_frame, text="❄️ تبريد السحب", bg="#0096c7", fg="white", command=self.toggle_fogging, **btn_style)
        self.btn_fogging.pack(side="right", padx=5)

        self.btn_water = tk.Button(ctrl_frame, text="💧 حقن الماء (Water)", bg="#1d3557", fg="white", command=self.toggle_water_injection, **btn_style)
        self.btn_water.pack(side="right", padx=5)

        self.btn_next = tk.Button(ctrl_frame, text="⏩ تطبيق والانتقال للجولة التالية", bg="#38b000", fg="white", command=self.next_round, **btn_style)
        self.btn_next.pack(side="left", padx=5)

    def log_message(self, text):
        self.log_box.insert("end", f">> {text}\n")
        self.log_box.see("end")

    def adjust_fuel(self, delta):
        if self.game_over:
            return
        self.fuel_valve = max(20.0, min(100.0, self.fuel_valve + delta))
        self.log_message(f"تم تعديل فتحة صمام الوقود إلى: {self.fuel_valve:.1f}%")
        self.update_simulation()

    def toggle_fogging(self):
        if self.game_over:
            return
        self.fogging = not self.fogging
        state_str = "تشغيل ❄️" if self.fogging else "إيقاف 🛑"
        self.log_message(f"تم {state_str} نظام تبريد هواء السحب بالرذاذ.")
        self.update_simulation()

    def toggle_water_injection(self):
        if self.game_over:
            return
        self.water_injection = not self.water_injection
        state_str = "تشغيل 💧" if self.water_injection else "إيقاف 🛑"
        self.log_message(f"تم {state_str} نظام حقن الماء لمكافحة الحرارة ورفع كثافة الغاز!")
        self.update_simulation()

    def update_simulation(self):
        cooling_effect = (25.0 if self.fogging else 0.0) + (45.0 if self.water_injection else 0.0)
        water_boost = 18.0 if self.water_injection else 0.0

        self.power_generated = (self.fuel_valve * 2.5) - (self.ambient_temp * 0.8) + (cooling_effect * 0.6) + water_boost
        self.egt_temp = 420.0 + (self.fuel_valve * 2.6) + (self.ambient_temp * 0.9) - cooling_effect
        self.vibration = 2.0 + (self.fuel_valve * 0.07) + (0.05 * (self.ambient_temp - 35))

        # تحديث النصوص
        self.lbl_power.config(text=f"طاقة التوليد الفعلية: {self.power_generated:.1f} MW (الهدف: {self.grid_demand:.0f} MW)")
        self.prog_power["value"] = self.power_generated

        egt_status = "طبيعي وآمن" if self.egt_temp < 600 else ("تحذير حرارة مرتفعة!" if self.egt_temp < 650 else "خطر شديد!")
        self.lbl_egt.config(text=f"حرارة غازات العادم EGT: {self.egt_temp:.1f} °C [{egt_status}]")
        self.prog_egt["value"] = self.egt_temp

        vib_status = "طبيعي" if self.vibration < 7.0 else ("إنذار اهتزاز!" if self.vibration < 9.0 else "خطر احتكاك الروتور!")
        self.lbl_vib.config(text=f"مستوى اهتزاز المحامل: {self.vibration:.2f} mm/s [{vib_status}]")
        self.prog_vib["value"] = self.vibration

        self.lbl_valve.config(text=f"صمام الوقود: {self.fuel_valve:.1f}%")
        if self.fogging:
            self.lbl_cooling.config(text="تبريد السحب: مُفعل ❄️", fg="#00f5d4")
        else:
            self.lbl_cooling.config(text="تبريد السحب: مُغلق 🛑", fg="#ff4d6d")

        if self.water_injection:
            self.lbl_water.config(text="حقن الماء: مُفعل 💧", fg="#00f5d4")
        else:
            self.lbl_water.config(text="حقن الماء: مُغلق 🛑", fg="#ff4d6d")

        # فحص كوارث الحماية
        if self.egt_temp >= 650.0:
            self.trigger_trip("🚨 إيقاف اضطراري كلي (EGT OVERHEAT TRIP)!", f"تجاوزت حرارة العادم الحد الأقصى ({self.egt_temp:.1f}°C > 650°C)! احترقت ريش التوربينة وتوقفت المحطة.")
        elif self.vibration >= 9.0:
            self.trigger_trip("🚨 إيقاف اضطراري للاهتزاز (HIGH VIBRATION TRIP)!", f"تجاوزت الاهتزازات الحد الخطر ({self.vibration:.2f} mm/s > 9.0 mm/s)! تم فصل التوربينة لحماية المحامل.")

    def trigger_trip(self, title, message):
        self.game_over = True
        self.log_message(f"🚨 {title}: {message}")
        messagebox.showerror(title, message + "\n\nانقطعت الكهرباء عن المدينة وفشلت النوبة!")

    def next_round(self):
        if self.game_over:
            return

        # حساب دقة التوليد
        diff = abs(self.power_generated - self.grid_demand)
        if diff <= 12.0:
            points = 20
            self.log_message(f"🌟 أداء ممتاز بالجولة {self.round_num}! طاقة التوليد تطابقت تماماً مع طلب الشبكة (+20 نقطة).")
        elif diff <= 30.0:
            points = 10
            self.log_message(f"👍 أداء جيد بالجولة {self.round_num}. تم تلبية معظم حمل الشبكة (+10 نقاط).")
        else:
            points = 0
            self.log_message(f"⚠️ عجز/فائض بالطاقة في الجولة {self.round_num} (فارق {diff:.1f} MW).")

        self.score += points
        self.lbl_score.config(text=f"النقاط: {self.score}")

        if self.round_num >= self.total_rounds:
            self.game_over = True
            msg = f"انتهت نوبة العمل بنجاح!\nمجموع نقاطك: {self.score} من 100.\n\n"
            if self.score >= 80:
                msg += "🏆 رتبتك: كبير مهندسي تشغيل التوربينات المعتمد!"
            elif self.score >= 50:
                msg += "🎖️ رتبتك: مهندس تشغيل محطات كفء."
            else:
                msg += "📝 رتبتك: مهندس متدرب يحتاج لمزيد من الموازنة."
            messagebox.showinfo("نهاية النوبة", msg)
            return

        # بدء جولة جديدة
        self.round_num += 1
        self.ambient_temp = random.choice([40.0, 47.0, 51.0, 44.0, 49.0])
        self.grid_demand = random.choice([145.0, 180.0, 215.0, 195.0, 160.0])

        self.lbl_round.config(text=f"الجولة: {self.round_num}/{self.total_rounds}")
        self.lbl_ambient.config(text=f"حرارة الجو: {self.ambient_temp:.0f}°C ☀️")
        self.lbl_demand.config(text=f"طلب الشبكة المستهدف: {self.grid_demand:.0f} MW ⚡")

        self.log_message(f"--- بدء الجولة {self.round_num}: طلب الشبكة الجديد {self.grid_demand:.0f} MW عند حرارة جو {self.ambient_temp:.0f}°C ---")
        self.update_simulation()

def main():
    root = tk.Tk()
    app = TurbineControlRoomApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
