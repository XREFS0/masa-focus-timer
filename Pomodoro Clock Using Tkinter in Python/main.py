"""
MASA 15_Pomodoro Clock Using Tkinter in Python with Source Code
Developer: MASA
"""

import tkinter as tk
import customtkinter as ctk
import math
import json
import time
from datetime import datetime
import os

# Appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class ProPomodoro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Clock")
        self.geometry("500x700")
        
        # State Variables
        self.reps = 0
        self.timer = None
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.total_time_for_session = 0
        
        # Default Settings
        self.work_mins = 25
        self.short_break = 5
        self.long_break = 20

        # --- Layout ---
        self.tabview = ctk.CTkTabview(self, width=450, height=650)
        self.tabview.pack(pady=10, padx=10)
        
        self.tab_timer = self.tabview.add("Timer")
        self.tab_tasks = self.tabview.add("Tasks & History")
        self.tab_settings = self.tabview.add("Settings")

        self.setup_timer_ui()
        self.setup_task_ui()
        self.setup_settings_ui()

    # ---------------------------- UI SECTIONS ------------------------------- #

    def setup_timer_ui(self):
        self.status_label = ctk.CTkLabel(self.tab_timer, text="Ready to Work?", font=("Roboto", 24))
        self.status_label.pack(pady=20)

        self.timer_label = ctk.CTkLabel(self.tab_timer, text="25:00", font=("Roboto", 90, "bold"))
        self.timer_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self.tab_timer, width=350)
        self.progress.set(1)
        self.progress.pack(pady=20)

        self.btn_start = ctk.CTkButton(self.tab_timer, text="Start Session", command=self.control_timer, height=50, font=("Roboto", 16, "bold"))
        self.btn_start.pack(pady=10)

        self.btn_reset = ctk.CTkButton(self.tab_timer, text="Reset", fg_color="transparent", border_width=2, command=self.reset_timer)
        self.btn_reset.pack(pady=5)

    def setup_task_ui(self):
        self.task_frame = ctk.CTkFrame(self.tab_tasks, fg_color="transparent")
        self.task_frame.pack(pady=10)

        self.task_entry = ctk.CTkEntry(self.task_frame, placeholder_text="Name your session...", width=250)
        self.task_entry.grid(row=0, column=0, padx=5)
        
        ctk.CTkLabel(self.tab_tasks, text="Session History", font=("Roboto", 16, "bold")).pack(pady=(10, 0))
        self.history_box = ctk.CTkTextbox(self.tab_tasks, width=400, height=350)
        self.history_box.pack(pady=10)
        
        self.history_btn_frame = ctk.CTkFrame(self.tab_tasks, fg_color="transparent")
        self.history_btn_frame.pack(pady=5)

        self.clear_btn = ctk.CTkButton(self.history_btn_frame, text="Clear History", 
                                       fg_color="#e74c3c", hover_color="#c0392b",
                                       command=self.clear_history, width=120)
        self.clear_btn.grid(row=0, column=0, padx=10)

        self.load_history()

    def setup_settings_ui(self):
        ctk.CTkLabel(self.tab_settings, text="Work Duration (min)").pack(pady=(10, 0))
        
        self.work_value_label = ctk.CTkLabel(self.tab_settings, text="25 min", font=("Roboto", 14, "bold"), text_color="#2ecc71")
        self.work_value_label.pack()

        self.work_slider = ctk.CTkSlider(self.tab_settings, from_=1, to=60, command=lambda v: self.update_times())
        self.work_slider.set(25)
        self.work_slider.pack(pady=10)

        ctk.CTkLabel(self.tab_settings, text="Break Duration (min)").pack(pady=(10, 0))
        
        self.break_value_label = ctk.CTkLabel(self.tab_settings, text="5 min", font=("Roboto", 14, "bold"), text_color="#3498db")
        self.break_value_label.pack()

        self.break_slider = ctk.CTkSlider(self.tab_settings, from_=1, to=30, command=lambda v: self.update_times())
        self.break_slider.set(5)
        self.break_slider.pack(pady=10)

    # ---------------------------- LOGIC ------------------------------- #

    def update_times(self):
        self.work_mins = int(self.work_slider.get())
        self.short_break = int(self.break_slider.get())
        
        self.work_value_label.configure(text=f"{self.work_mins} min")
        self.break_value_label.configure(text=f"{self.short_break} min")

        if not self.is_running:
            self.timer_label.configure(text=f"{self.work_mins:02d}:00")

    def control_timer(self):
        if not self.is_running:
            self.start_new_session()
        elif self.is_paused:
            self.resume_timer()
        else:
            self.pause_timer()

    def start_new_session(self):
        self.is_running = True
        self.is_paused = False
        self.reps += 1
        
        if self.reps % 8 == 0:
            self.remaining_time = self.long_break * 60
            self.status_label.configure(text="Long Break", text_color="#3498db")
        elif self.reps % 2 == 0:
            self.remaining_time = self.short_break * 60
            self.status_label.configure(text="Short Break", text_color="#e67e22")
        else:
            self.remaining_time = self.work_mins * 60
            self.status_label.configure(text="Deep Focus", text_color="#2ecc71")
        
        self.total_time_for_session = self.remaining_time
        self.btn_start.configure(text="Pause", fg_color="#e74c3c")
        self.run_countdown()

    def pause_timer(self):
        self.is_paused = True
        self.btn_start.configure(text="Resume", fg_color="#f1c40f")
        if self.timer:
            self.after_cancel(self.timer)

    def resume_timer(self):
        self.is_paused = False
        self.btn_start.configure(text="Pause", fg_color="#e74c3c")
        self.run_countdown()

    def run_countdown(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        
        if self.total_time_for_session > 0:
            self.progress.set(self.remaining_time / self.total_time_for_session)

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer = self.after(1000, self.run_countdown)
        else:
            # STOPPED: No longer automatically calls start_new_session
            self.session_complete()

    def session_complete(self):
        self.is_running = False
        self.bell() 
        self.status_label.configure(text="Session Finished!", text_color="#ffffff")
        self.btn_start.configure(text="Start Next", fg_color="#2ecc71")
        
        if self.reps % 2 != 0: 
            self.log_session()

    def reset_timer(self):
        if self.timer:
            self.after_cancel(self.timer)
        self.is_running = False
        self.reps = 0
        self.update_times()
        self.progress.set(1)
        self.status_label.configure(text="Ready to Work?", text_color="#ffffff")
        self.btn_start.configure(text="Start Session", fg_color=["#2CC985", "#2FA572"])

    def log_session(self):
        # Named session logic
        task = self.task_entry.get() or f"Session {math.ceil(self.reps/2)}"
        timestamp = datetime.now().strftime("%H:%M")
        log_entry = f"[{timestamp}] {task}\n"
        
        self.history_box.insert("0.0", log_entry)
        
        with open("history.txt", "a") as f:
            f.write(log_entry)

    def load_history(self):
        try:
            if os.path.exists("history.txt"):
                with open("history.txt", "r") as f:
                    content = f.read()
                    self.history_box.delete("0.0", "end")
                    self.history_box.insert("0.0", content)
        except Exception:
            pass

    def clear_history(self):
        self.history_box.delete("0.0", "end")
        if os.path.exists("history.txt"):
            os.remove("history.txt")

if __name__ == "__main__":
    app = ProPomodoro()
    app.mainloop()