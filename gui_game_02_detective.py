# -*- coding: utf-8 -*-
"""
لعبة واجهة رسومية حقيقية: المحقق الهندسي لكشف أعطال التوربينات (Diagnostic Detective GUI)
========================================================================================
واجهة رسومية تفاعلية تدعم اللغة العربية بالكامل بدون أي مشاكل في الخطوط أو موجهات الأوامر.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox

CASES = [
    {
        "id": 1,
        "title": "القضية #1: لغز اهتزازات ضاغط غاز الرميلة",
        "location": "حقل الرميلة - قطار ضغط الغاز المصاحب",
        "alarm": "إنذار عاجل: اهتزازات جانبية شديدة ومفاجئة على المحمل رقم 2 بعد الإقلاع بسرعة 3000 RPM.",
        "tests": {
            "1": ("طيف الاهتزازات الترددي (FFT)", 2, "قمة اهتزاز عملاقة وحيدة عند التردد الأساسي 1X (50.0 Hz) تتناسب طردياً مع مربع سرعة الدوران. زوايا الطور ثابتة تماماً."),
            "2": ("تحليل عينة زيت التزييت", 2, "لزوجة الزيت ممتازة، لا توجد أي برادة معدنية من النحاس أو الحديد. الزيت نظيف وخالٍ من الرطوبة."),
            "3": ("فحص كاميرا البورسكوب البصرية", 3, "ريش الضاغط سليمة وخالية من الكسور، لكن لوحظ فقدان وتطاير أحد أوزان الموازنة الطرفية على قرص الدوران."),
            "4": ("فحص انتشار درجات حرارة العادم", 2, "توزيع درجات الحرارة متجانس وفارق المجسات أقل من 8°C (الاحتراق سليم بنسبة 100%).")
        },
        "options": [
            "دوامة الزيت الهيدروديناميكية في المحامل (Oil Whirl Instability)",
            "انعدام الموازنة الكتلية للروتور (Rotor Mass Unbalance)",
            "انسداد وتفحم حواقن الوقود (Fuel Nozzle Clogging)",
            "عدم محاذاة عمود الدوران (Shaft Misalignment 2X)"
        ],
        "correct_idx": 1,
        "explanation": "ظهور قمة اهتزاز مهيمنة بدقة عند 1X مع فقدان وزن الموازنة يؤكد وجود Unbalance خالص (ISO 1940)."
    },
    {
        "id": 2,
        "title": "القضية #2: هبوط طاقة توربينة شط البصرة 9FA",
        "location": "محطة كهرباء شط البصرة الغازية (250 MW)",
        "alarm": "هبوط مفاجئ في القدرة بمقدار 18 MW مع قفزة غير مسبوقة في فرق درجات حرارة العادم (Temp Spread > 45°C).",
        "tests": {
            "1": ("طيف الاهتزازات الترددي (FFT)", 2, "الاهتزازات الكلية طبيعية ومستقرة تحت 2.1 mm/s، ولا توجد أي ترددات رنينية شاذة."),
            "2": ("تحليل عينة زيت التزييت", 2, "الزيت سليم ودرجة حرارته طبيعية (52°C) ضمن الحدود التصميمية."),
            "3": ("فحص كاميرا البورسكوب البصرية", 3, "انسداد جزئي وتفحم كربوني شديد على فوهة حاقن الوقود في غرفة الاحتراق رقم 7 (Combustor Can #7)."),
            "4": ("فحص ضغط حجرة الاحتراق وتدفق الغاز", 2, "انخفاض تدفق الغاز في المغذي رقم 7 بنسبة 40% مما شكل بقعة باردة موضعية في العادم.")
        },
        "options": [
            "كسر في ريش المرحلة الأولى للتوربينة (HPT Blade Fracture)",
            "احتكاك الروتور بالمحمل الخارجي (Rotor Rubbing)",
            "انسداد وتفحم حاقن وقود غرفة الاحتراق (Fuel Nozzle Carbon Clogging)",
            "انهيار طبقة التخميد في محامل كابوني (Capone Bearing Failure)"
        ],
        "correct_idx": 2,
        "explanation": "الـ Temp Spread المرتفع في العادم هو التوقيع الحاسم لعدم انتظام الاحتراق بسبب انسداد حاقن الوقود."
    },
    {
        "id": 3,
        "title": "القضية #3: اضطراب التوربينة البخارية بالهارثة",
        "location": "محطة كهرباء الهارثة الحرارية - توربينة بخارية منخفضة الضغط (LP)",
        "alarm": "اهتزازات تذبذبية غير مستقرة بتردد منخفض (Subharmonic) عند السرعات العالية مع سخونة المحمل الانزلاقي.",
        "tests": {
            "1": ("طيف الاهتزازات الترددي (FFT)", 2, "ظهور تردد تحت متزامن بارز عند 0.46X (حوالي 23 Hz عند سرعة 50 Hz)، مصحوباً بمدار اهتزاز بيضاوي متسع."),
            "2": ("تحليل عينة زيت التزييت", 2, "انخفاض حاد في لزوجة الزيت وارتفاع حرارته إلى 85°C مما قلل من لزوجة إسفين الزيت الهيدروديناميكي."),
            "3": ("فحص كاميرا البورسكوب البصرية", 3, "ريش التوربينة البخارية سليمة، لكن لوحظ انزلاق طبقة التزييت في المحمل الانزلاقي."),
            "4": ("فحص الخلوص الرأسي للمحمل", 2, "اتساع الخلوص الرأسي فوق الحد المسموح به مما يسهل طواف عمود الدوران داخل غشاء الزيت.")
        },
        "options": [
            "دوامة وتذبذب غشاء الزيت الهيدروديناميكي (Oil Whirl / Whip Instability)",
            "تآكل الريش بقطرات البخار الرطب (Water Droplet Erosion)",
            "انكسار ريشة الدوران الأخيرة (L-0 Blade Loss)",
            "تفكك براغي تثبيت القاعدة الأرضية (Loose Foundation Bolts)"
        ],
        "correct_idx": 0,
        "explanation": "التردد تحت المتزامن عند ~0.46X مع تدهور لزوجة الزيت هو التوقيع الرياضي الكلاسيكي لعدم استقرار طبقة الزيت (Oil Whirl)."
    }
]

class DetectiveGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕵️‍♂️ المحقق الهندسي: كاشف أعطال التوربينات (Diagnostic Detective GUI)")
        self.root.geometry("820x760")
        self.root.configure(bg="#1a1d24")
        self.root.resizable(False, False)

        self.current_case_idx = 0
        self.hours_left = 5
        self.total_score = 0
        self.seen_tests = set()

        self.setup_ui()
        self.load_case()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2b2d42", pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🕵️‍♂️ المركز الوطني لتشخيص أعطال التوربينات ومحطات الطاقة",
            font=("Segoe UI", 16, "bold"),
            fg="#edf2f4",
            bg="#2b2d42"
        ).pack()

        # Case info box
        case_frame = tk.LabelFrame(
            self.root,
            text=" 🚨 البلاغ الفني الطارئ ",
            font=("Segoe UI", 12, "bold"),
            fg="#ef233c",
            bg="#21252f",
            padx=15,
            pady=10
        )
        case_frame.pack(fill="x", padx=20, pady=8)

        self.lbl_case_title = tk.Label(case_frame, text="", font=("Segoe UI", 13, "bold"), fg="#ffffff", bg="#21252f")
        self.lbl_case_title.pack(anchor="e")

        self.lbl_case_loc = tk.Label(case_frame, text="", font=("Segoe UI", 10), fg="#8d99ae", bg="#21252f")
        self.lbl_case_loc.pack(anchor="e", pady=2)

        self.lbl_case_alarm = tk.Label(case_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffb703", bg="#21252f", wraplength=760, justify="right")
        self.lbl_case_alarm.pack(anchor="e", pady=4)

        # Budget & Score status
        bar = tk.Frame(self.root, bg="#1a1d24", pady=5)
        bar.pack(fill="x", padx=20)

        self.lbl_hours = tk.Label(bar, text="ساعات الفحص المتاحة: 5 ساعات ⏳", font=("Segoe UI", 12, "bold"), fg="#00f5d4", bg="#343a40", padx=12, pady=4)
        self.lbl_hours.pack(side="right", padx=5)

        self.lbl_score = tk.Label(bar, text="مجموع النقاط: 0 🏆", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#7209b7", padx=12, pady=4)
        self.lbl_score.pack(side="left", padx=5)

        # Laboratory Tests Frame
        tests_frame = tk.LabelFrame(
            self.root,
            text=" 🔬 الفحوصات المخبرية المتاحة (اختر فحصاً لإجرائه) ",
            font=("Segoe UI", 12, "bold"),
            fg="#00d2ff",
            bg="#21252f",
            padx=15,
            pady=10
        )
        tests_frame.pack(fill="x", padx=20, pady=6)

        self.btn_tests = {}
        for k in ["1", "2", "3", "4"]:
            btn = tk.Button(
                tests_frame,
                text="",
                font=("Segoe UI", 10, "bold"),
                bg="#0077b6",
                fg="white",
                cursor="hand2",
                command=lambda key=k: self.run_test(key)
            )
            btn.pack(fill="x", pady=3)
            self.btn_tests[k] = btn

        # Findings display
        self.txt_result = tk.Text(self.root, height=5, font=("Segoe UI", 10), bg="#0f1117", fg="#70e000", wrap="word", padx=10, pady=8)
        self.txt_result.pack(fill="x", padx=20, pady=6)

        # Final Verdict Decision Frame
        verdict_frame = tk.LabelFrame(
            self.root,
            text=" ⚖️ القرار التشخيصي النهائي (ما هو السبب الجذري؟) ",
            font=("Segoe UI", 12, "bold"),
            fg="#ffd166",
            bg="#21252f",
            padx=15,
            pady=10
        )
        verdict_frame.pack(fill="x", padx=20, pady=6)

        self.verdict_var = tk.IntVar(value=-1)
        self.radio_opts = []
        for i in range(4):
            rb = tk.Radiobutton(
                verdict_frame,
                text="",
                variable=self.verdict_var,
                value=i,
                font=("Segoe UI", 10, "bold"),
                fg="#ffffff",
                bg="#21252f",
                selectcolor="#023e8a",
                activebackground="#21252f",
                activeforeground="#00d2ff",
                anchor="e",
                justify="right"
            )
            rb.pack(fill="x", pady=2)
            self.radio_opts.append(rb)

        btn_submit = tk.Button(
            self.root,
            text="🎯 إصدار القرار الهندسي النهائي واعتماده",
            font=("Segoe UI", 12, "bold"),
            bg="#38b000",
            fg="white",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.submit_verdict
        )
        btn_submit.pack(pady=10)

    def load_case(self):
        case = CASES[self.current_case_idx]
        self.hours_left = 5
        self.seen_tests.clear()
        self.verdict_var.set(-1)

        self.lbl_case_title.config(text=case["title"])
        self.lbl_case_loc.config(text=f"📍 الموقع: {case['location']}")
        self.lbl_case_alarm.config(text=case["alarm"])
        self.lbl_hours.config(text=f"ساعات الفحص المتاحة: {self.hours_left} ساعات ⏳")

        self.txt_result.delete("1.0", "end")
        self.txt_result.insert("end", ">> اختر فحصاً من القائمة أعلاه لمعاينة تقرير المختبر الفني...\n")

        for k, (name, cost, _) in case["tests"].items():
            self.btn_tests[k].config(text=f"[{k}] {name} (يكلف {cost} ساعات فحص)", state="normal", bg="#0077b6")

        for i, opt_text in enumerate(case["options"]):
            self.radio_opts[i].config(text=opt_text)

    def run_test(self, key):
        case = CASES[self.current_case_idx]
        name, cost, result_text = case["tests"][key]

        if key in self.seen_tests:
            messagebox.showinfo("فحص مكرر", "أجريت هذا الفحص مسبقاً! النتيجة مدونة في الأسفل.")
            return

        if cost > self.hours_left:
            messagebox.showwarning("ميزانية غير كافية", f"هذا الفحص يتطلب {cost} ساعات، وميزانيتك المتبقية {self.hours_left} ساعات فقط!")
            return

        self.hours_left -= cost
        self.seen_tests.add(key)
        self.lbl_hours.config(text=f"ساعات الفحص المتاحة: {self.hours_left} ساعات ⏳")
        self.btn_tests[key].config(state="disabled", bg="#3a5a40", text=f"✅ {name} [تم الفحص بنجاح]")

        self.txt_result.delete("1.0", "end")
        self.txt_result.insert("end", f"🔬 تقرير المختبر - {name}:\n>> {result_text}\n")

    def submit_verdict(self):
        chosen = self.verdict_var.get()
        if chosen == -1:
            messagebox.showwarning("تنبيه", "يرجى اختيار أحد الخيارات التشخيصية أولاً!")
            return

        case = CASES[self.current_case_idx]
        if chosen == case["correct_idx"]:
            self.total_score += 35
            self.lbl_score.config(text=f"مجموع النقاط: {self.total_score} 🏆")
            messagebox.showinfo(
                "تشخيص عبقري وناجح! 🌟",
                f"أحسنت! إجابة صحيحة تماماً تم على إثرها إنقاذ المحطة (+35 نقطة).\n\n💡 التفسير الهندسي:\n{case['explanation']}"
            )
        else:
            correct_name = case["options"][case["correct_idx"]]
            messagebox.showerror(
                "تشخيص خاطئ للأسف! ❌",
                f"التشخيص كان غير دقيق وكلف المحطة أضراراً جسيمة.\n\nالسبب الحقيقي كان:\n{correct_name}\n\n💡 التفسير الهندسي:\n{case['explanation']}"
            )

        if self.current_case_idx < len(CASES) - 1:
            self.current_case_idx += 1
            self.load_case()
        else:
            self.finish_game()

    def finish_game(self):
        msg = f"انتهت جميع القضايا الهندسية!\nمجموع نقاطك النهائي: {self.total_score} من 105.\n\n"
        if self.total_score >= 100:
            msg += "🏆 رتبتك: أستاذ التشخيص والاهتزازات العالمي (Master Diagnostician)!"
        elif self.total_score >= 70:
            msg += "🎖️ رتبتك: كبير مهندسي صيانة موثوق (Senior Specialist)."
        else:
            msg += "📚 تحتاج لمزيد من الممارسة في تحليل أطياف الاهتزازات والزيوت."
        messagebox.showinfo("التقرير الختامي للمحقق", msg)

def main():
    root = tk.Tk()
    app = DetectiveGameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
