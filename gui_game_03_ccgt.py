# -*- coding: utf-8 -*-
"""
لعبة واجهة رسومية حقيقية: مهندس الدورة المركبة الكبرى (CCGT Master GUI)
======================================================================
واجهة رسومية ديناميكية تدعم اللغة العربية بالكامل مع مزلقات تحكم (Sliders) حية
لمحاكاة الديناميكا الحرارية لمحطات الدورة المركبة (برايتون + رانكن).
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox

class CCGTMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ مهندس محطة الدورة المركبة الكبرى (Combined Cycle CCGT Master)")
        self.root.geometry("780x760")
        self.root.configure(bg="#1a1d24")
        self.root.resizable(False, False)

        # المتغيرات الهندسية
        self.var_rp = tk.DoubleVar(value=16.0)
        self.var_firing = tk.DoubleVar(value=1280.0)
        self.var_steam_p = tk.DoubleVar(value=95.0)
        self.var_duct = tk.BooleanVar(value=False)
        self.best_eff = 0.0

        self.setup_ui()
        self.recalculate()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#240046", pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="⚡ مختبر تصميم محطات الدورة المركبة الهجينة (CCGT)",
            font=("Segoe UI", 16, "bold"),
            fg="#e0aaff",
            bg="#240046"
        ).pack()

        # Goal Banner
        goal_frame = tk.Frame(self.root, bg="#10002b", pady=6)
        goal_frame.pack(fill="x")
        tk.Label(
            goal_frame,
            text="🎯 الهدف الهندسي: وازن المتغيرات لتجاوز حاجز الـ 60% كفاءة حرارية وتحقيق أعلى ربح تجاري!",
            font=("Segoe UI", 11, "bold"),
            fg="#ffd166",
            bg="#10002b"
        ).pack()

        # Sliders Frame
        sliders_frame = tk.LabelFrame(
            self.root,
            text=" 🛠️ أدوات التحكم التصميمية (حرّك المؤشرات وشاهد التغير اللحظي) ",
            font=("Segoe UI", 12, "bold"),
            fg="#00d2ff",
            bg="#21252f",
            padx=20,
            pady=15
        )
        sliders_frame.pack(fill="x", padx=20, pady=10)

        # 1. Pressure Ratio
        self.lbl_rp_val = tk.Label(sliders_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_rp_val.pack(anchor="e")
        scale_rp = ttk.Scale(sliders_frame, from_=12.0, to=24.0, variable=self.var_rp, orient="horizontal", length=700, command=lambda v: self.recalculate())
        scale_rp.pack(pady=4)

        # 2. Firing Temp
        self.lbl_firing_val = tk.Label(sliders_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_firing_val.pack(anchor="e")
        scale_firing = ttk.Scale(sliders_frame, from_=1100.0, to=1450.0, variable=self.var_firing, orient="horizontal", length=700, command=lambda v: self.recalculate())
        scale_firing.pack(pady=4)

        # 3. Steam Pressure
        self.lbl_steam_val = tk.Label(sliders_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_steam_val.pack(anchor="e")
        scale_steam = ttk.Scale(sliders_frame, from_=40.0, to=140.0, variable=self.var_steam_p, orient="horizontal", length=700, command=lambda v: self.recalculate())
        scale_steam.pack(pady=4)

        # 4. Duct Firing Toggle
        chk_duct = tk.Checkbutton(
            sliders_frame,
            text="🔥 تفعيل الحرق الإضافي داخل قناة المرجل (Duct Firing) لزيادة إنتاج البخار",
            variable=self.var_duct,
            font=("Segoe UI", 11, "bold"),
            fg="#ffb703",
            bg="#21252f",
            selectcolor="#343a40",
            activebackground="#21252f",
            activeforeground="#ffb703",
            command=self.recalculate
        )
        chk_duct.pack(anchor="e", pady=8)

        # Outputs Frame
        out_frame = tk.LabelFrame(
            self.root,
            text=" 📊 نتائج الأداء التشغيلي والجدوى الاقتصادية ",
            font=("Segoe UI", 12, "bold"),
            fg="#06d6a0",
            bg="#21252f",
            padx=20,
            pady=15
        )
        out_frame.pack(fill="x", padx=20, pady=10)

        # Efficiency Display & Gauge
        self.lbl_eff = tk.Label(out_frame, text="", font=("Segoe UI", 16, "bold"), fg="#00f5d4", bg="#21252f")
        self.lbl_eff.pack(pady=4)

        self.prog_eff = ttk.Progressbar(out_frame, orient="horizontal", length=700, mode="determinate", maximum=65.0)
        self.prog_eff.pack(pady=6)

        # Grid of outputs
        grid_frame = tk.Frame(out_frame, bg="#21252f")
        grid_frame.pack(fill="x", pady=8)

        self.lbl_gt_power = tk.Label(grid_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#2b303c", padx=12, pady=6)
        self.lbl_gt_power.grid(row=0, column=0, padx=6, pady=4, sticky="ew")

        self.lbl_st_power = tk.Label(grid_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#2b303c", padx=12, pady=6)
        self.lbl_st_power.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        self.lbl_tot_power = tk.Label(grid_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffd166", bg="#2b303c", padx=12, pady=6)
        self.lbl_tot_power.grid(row=1, column=0, padx=6, pady=4, sticky="ew")

        self.lbl_profit = tk.Label(grid_frame, text="", font=("Segoe UI", 11, "bold"), fg="#70e000", bg="#2b303c", padx=12, pady=6)
        self.lbl_profit.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Evaluation Button
        btn_eval = tk.Button(
            self.root,
            text="🏆 اعتماد هذا التصميم الهندسي وتقييم النتيجة الرسمية",
            font=("Segoe UI", 12, "bold"),
            bg="#7209b7",
            fg="white",
            cursor="hand2",
            padx=15,
            pady=10,
            command=self.evaluate_design
        )
        btn_eval.pack(pady=10)

    def recalculate(self):
        rp = self.var_rp.get()
        firing = self.var_firing.get()
        steam_p = self.var_steam_p.get()
        duct = self.var_duct.get()

        self.lbl_rp_val.config(text=f"نسبة انضغاط الضاغط (Pressure Ratio rp): {rp:.1f}")
        self.lbl_firing_val.config(text=f"درجة حرارة مدخل التوربينة (Firing Temp TIT): {firing:.0f} °C")
        self.lbl_steam_val.config(text=f"ضغط بخار مرجل الـ HRSG (Steam Pressure): {steam_p:.0f} bar")

        # الحسابات الهندسية
        gamma = 1.4
        t_ambient_k = 303.15  # 30°C
        t_comp_out_k = t_ambient_k * (rp ** ((gamma - 1) / gamma))
        
        t_fire_k = firing + 273.15
        q_fuel_mw = (t_fire_k - t_comp_out_k) * 0.45
        gt_power_mw = q_fuel_mw * (1.0 - (t_ambient_k / t_comp_out_k) * 0.92)
        gt_power_mw = max(110.0, min(360.0, gt_power_mw))

        # HRSG & Steam
        heat_in_exhaust_mw = q_fuel_mw - gt_power_mw
        extra_duct_fuel = 45.0 if duct else 0.0
        steam_heat_mw = (heat_in_exhaust_mw * 0.83) + (extra_duct_fuel * 0.90)

        steam_cycle_eff = 0.31 + (steam_p / 140.0) * 0.09
        st_power_mw = steam_heat_mw * steam_cycle_eff

        total_fuel_mw = q_fuel_mw + extra_duct_fuel
        total_power_mw = gt_power_mw + st_power_mw
        ccgt_eff = (total_power_mw / total_fuel_mw) * 100.0

        revenue = total_power_mw * 55.0
        cost = total_fuel_mw * 16.5
        profit = revenue - cost

        # تحديث الواجهة
        if ccgt_eff > self.best_eff:
            self.best_eff = ccgt_eff

        eff_badge = "🏆 تجاوزت 60% كفاءة عالمية!" if ccgt_eff >= 60.0 else ("ممتازة جداً 👍" if ccgt_eff >= 57.0 else "جيدة")
        self.lbl_eff.config(text=f"الكفاءة الحرارية المجمعة للمحطة (CCGT Efficiency): {ccgt_eff:.2f}% [{eff_badge}]")
        self.prog_eff["value"] = ccgt_eff

        self.lbl_gt_power.config(text=f"طاقة التوربينة الغازية: {gt_power_mw:.1f} MW")
        self.lbl_st_power.config(text=f"طاقة التوربينة البخارية: {st_power_mw:.1f} MW")
        self.lbl_tot_power.config(text=f"إجمالي القدرة المولدة: {total_power_mw:.1f} MW")
        self.lbl_profit.config(text=f"صافي الأرباح التشغيلية: {profit:,.0f} $/ساعة 💰")

    def evaluate_design(self):
        rp = self.var_rp.get()
        firing = self.var_firing.get()
        steam_p = self.var_steam_p.get()
        ccgt_eff = self.prog_eff["value"]

        msg = f"تقرير اعتماد التصميم الهندسي:\n"
        msg += f"- نسبة الانضغاط: {rp:.1f}\n"
        msg += f"- حرارة الاحتراق: {firing:.0f}°C\n"
        msg += f"- ضغط البخار: {steam_p:.0f} bar\n"
        msg += f"- الكفاءة المحققة: {ccgt_eff:.2f}%\n\n"

        if ccgt_eff >= 60.0:
            msg += "🏆 مبروك! حققت رقماً قياسياً عالمياً واعتُمدت كبيراً لمهندسي دورات الطاقة العالمية (Chief CCGT Architect)!"
            messagebox.showinfo("إنجاز عالمي ممتاز", msg)
        elif ccgt_eff >= 57.0:
            msg += "🎖️ تصميم عالي الكفاءة ينافس أحدث محطات سيمنز وجنرال إلكتريك!"
            messagebox.showinfo("تصميم ناجح", msg)
        else:
            msg += "💡 نصيحة: ارفع حرارة الاحتراق وضغط البخار قليلاً لرفع كفاءة دورة رانكن البخارية."
            messagebox.showinfo("نتائج التقييم", msg)

def main():
    root = tk.Tk()
    app = CCGTMasterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
