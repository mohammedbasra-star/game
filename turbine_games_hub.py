# -*- coding: utf-8 -*-
"""
مركز ألعاب التوربينات - الشاشة الرئيسية (Turbomachinery Games Hub)
==================================================================
واجهة رسومية موحدة تتيح لك تشغيل أي لعبة من ألعاب التوربينات بضغطة زر واحدة وبخط عربي سليم.
"""

import sys
import os
import subprocess
import tkinter as tk

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def launch_game(script_name):
    script_path = os.path.join(CURRENT_DIR, script_name)
    subprocess.Popen([sys.executable, script_path])

def main():
    root = tk.Tk()
    root.title("🎮 مركز ألعاب التوربينات - بايثون")
    root.geometry("640x560")
    root.configure(bg="#161a1d")
    root.resizable(False, False)

    # Header
    header = tk.Frame(root, bg="#0b090a", pady=15)
    header.pack(fill="x")
    tk.Label(
        header,
        text="🎮 مركز ألعاب التوربينات الهندسية",
        font=("Segoe UI", 18, "bold"),
        fg="#e5383b",
        bg="#0b090a"
    ).pack()
    tk.Label(
        header,
        text="اختر اللعبة التي تريد خوض تحديها الآن بنقرة زر واحدة",
        font=("Segoe UI", 11),
        fg="#b1a7a6",
        bg="#0b090a"
    ).pack(pady=4)

    cards_frame = tk.Frame(root, bg="#161a1d", pady=20)
    cards_frame.pack(fill="both", expand=True, padx=30)

    btn_style = {
        "font": ("Segoe UI", 12, "bold"),
        "fg": "white",
        "cursor": "hand2",
        "padx": 15,
        "pady": 12,
        "bd": 0
    }

    # Game 1 Button
    f1 = tk.Frame(cards_frame, bg="#212529", pady=6, padx=10)
    f1.pack(fill="x", pady=8)
    tk.Button(
        f1,
        text="🏭 [اللعبة 1] مشغّل غرفة التحكم (Control Room Operator)",
        bg="#0077b6",
        command=lambda: launch_game("gui_game_01_control_room.py"),
        **btn_style
    ).pack(fill="x")
    tk.Label(
        f1,
        text="وازن صمام الوقود والتبريد لتوليد الميجاواط ومنع الإيقاف الاضطراري (Trip)",
        font=("Segoe UI", 9),
        fg="#ced4da",
        bg="#212529"
    ).pack(pady=2)

    # Game 2 Button
    f2 = tk.Frame(cards_frame, bg="#212529", pady=6, padx=10)
    f2.pack(fill="x", pady=8)
    tk.Button(
        f2,
        text="🕵️‍♂️ [اللعبة 5] المحقق الهندسي للأعطال (Diagnostic Detective)",
        bg="#6a040f",
        command=lambda: launch_game("gui_game_02_detective.py"),
        **btn_style
    ).pack(fill="x")
    tk.Label(
        f2,
        text="حل قضايا الأعطال الطارئة في المحطات واكتشف السبب الجذري عبر أطياف الاهتزاز والزيوت",
        font=("Segoe UI", 9),
        fg="#ced4da",
        bg="#212529"
    ).pack(pady=2)

    # Game 3 Button
    f3 = tk.Frame(cards_frame, bg="#212529", pady=6, padx=10)
    f3.pack(fill="x", pady=8)
    tk.Button(
        f3,
        text="⚡ [اللعبة 9] مهندس الدورة المركبة الكبرى (CCGT Master)",
        bg="#5a189a",
        command=lambda: launch_game("gui_game_03_ccgt.py"),
        **btn_style
    ).pack(fill="x")
    tk.Label(
        f3,
        text="صمم محطة CCGT هجينة وحرّك المؤشرات لكسر حاجز كفاءة الـ 60% العالمية",
        font=("Segoe UI", 9),
        fg="#ced4da",
        bg="#212529"
    ).pack(pady=2)

    root.mainloop()

if __name__ == "__main__":
    main()
