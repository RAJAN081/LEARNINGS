import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from datetime import datetime, timedelta
import pygame

# Initialize pygame mixer for audio
pygame.mixer.init()

# Function to play alarm sound
def play_sound():
    pygame.mixer.music.load("alarm-sound-21949.mp3")
    pygame.mixer.music.play()

# Main App Class
class AlarmStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm & Stopwatch")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e2f")

        # Initialize Variables
        self.alarms = []
        self.stopwatch_running = False
        self.stopwatch_time = 0

        # Create Pages
        self.alarm_page = tk.Frame(self.root, bg="#1e1e2f")
        self.stopwatch_page = tk.Frame(self.root, bg="#1e1e2f")
        self.active_page = self.alarm_page

        # Build Pages
        self.create_alarm_page()
        self.create_stopwatch_page()

        # Circular Page Switcher
        self.page_switcher = tk.Button(
            self.root, text="⭮", font=("Helvetica", 18), bg="#00ffcc", fg="#1e1e2f",
            relief="flat", command=self.switch_page, width=4, height=2
        )
        self.page_switcher.place(x=10, y=10)

        # Show Initial Page
        self.alarm_page.pack(fill=tk.BOTH, expand=True)

    def switch_page(self):
        self.active_page.pack_forget()
        self.active_page = self.stopwatch_page if self.active_page == self.alarm_page else self.alarm_page
        self.active_page.pack(fill=tk.BOTH, expand=True)

    def create_alarm_page(self):
        # Alarm Title
        tk.Label(
            self.alarm_page, text="Alarm Clock", font=("Helvetica", 18), fg="#00ffcc", bg="#1e1e2f"
        ).pack(pady=10)

        # Alarm Input Section
        input_frame = tk.Frame(self.alarm_page, bg="#1e1e2f")
        input_frame.pack(pady=20)

        # Hour, Minute, AM/PM Dropdowns
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.ampm_var = tk.StringVar()
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.ampm_var.set("AM")

        hours = [f"{i:02}" for i in range(1, 13)]
        minutes = [f"{i:02}" for i in range(0, 60)]
        ampm = ["AM", "PM"]

        ttk.Combobox(input_frame, textvariable=self.hour_var, values=hours, width=8, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        ttk.Combobox(input_frame, textvariable=self.minute_var, values=minutes, width=8, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        ttk.Combobox(input_frame, textvariable=self.ampm_var, values=ampm, width=8, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        # Set Alarm Button
        tk.Button(
            input_frame, text="Set Alarm", command=self.set_alarm, bg="#00ffcc", fg="#1e1e2f", font=("Helvetica", 12), width=10
        ).pack(side=tk.LEFT, padx=10)

        # Active Alarms Section
        alarm_frame = tk.Frame(self.alarm_page, bg="#1e1e2f", relief="ridge", bd=2)
        alarm_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(
            alarm_frame, text="Active Alarms", font=("Helvetica", 14), fg="#00ffcc", bg="#1e1e2f"
        ).pack(pady=5)
        self.alarm_display = tk.Text(
            alarm_frame, height=10, width=30, font=("Helvetica", 14), bg="#1e1e2f", fg="#00ffcc", state=tk.DISABLED
        )
        self.alarm_display.pack(pady=10)

    def set_alarm(self):
        try:
            # Parse Alarm Time
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            ampm = self.ampm_var.get()
            if ampm == "PM" and hour != 12:
                hour += 12
            elif ampm == "AM" and hour == 12:
                hour = 0

            current_time = datetime.now()
            alarm_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if alarm_time < current_time:
                alarm_time += timedelta(days=1)

            # Add Alarm to List
            self.alarms.append(alarm_time)
            self.update_alarm_display()

            # Start Alarm Thread
            threading.Thread(target=self.wait_for_alarm, args=(alarm_time,)).start()

        except ValueError:
            messagebox.showerror("Error", "Invalid time format!")

    def wait_for_alarm(self, alarm_time):
        time_to_wait = (alarm_time - datetime.now()).total_seconds()
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        play_sound()
        messagebox.showinfo("Alarm", f"Alarm for {alarm_time.strftime('%I:%M %p')} is ringing!")
        self.alarms.remove(alarm_time)
        self.update_alarm_display()

    def update_alarm_display(self):
        self.alarm_display.config(state=tk.NORMAL)
        self.alarm_display.delete("1.0", tk.END)
        for alarm in self.alarms:
            self.alarm_display.insert(tk.END, f"{alarm.strftime('%I:%M %p')}\n")
        self.alarm_display.config(state=tk.DISABLED)

    def create_stopwatch_page(self):
        # Stopwatch Title
        tk.Label(
            self.stopwatch_page, text="Stopwatch", font=("Helvetica", 18), fg="#00ffcc", bg="#1e1e2f"
        ).pack(pady=10)

        # Stopwatch Display
        self.stopwatch_label = tk.Label(
            self.stopwatch_page, text="00:00:00.000", font=("Helvetica", 28), fg="#ffffff", bg="#ff6666"
        )
        self.stopwatch_label.pack(pady=20)

        # Stopwatch Buttons
        button_frame = tk.Frame(self.stopwatch_page, bg="#1e1e2f")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Start", command=self.start_stopwatch, bg="green", fg="#ffffff", font=("Helvetica", 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Stop", command=self.stop_stopwatch, bg="red", fg="#ffffff", font=("Helvetica", 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Reset", command=self.reset_stopwatch, bg="blue", fg="#ffffff", font=("Helvetica", 12), width=10).pack(side=tk.LEFT, padx=10)

    def start_stopwatch(self):
        self.stopwatch_running = True
        self.update_stopwatch()

    def stop_stopwatch(self):
        self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.stopwatch_label.config(text="00:00:00.000")

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_time += 10
            milliseconds = self.stopwatch_time % 1000
            seconds = (self.stopwatch_time // 1000) % 60
            minutes = (self.stopwatch_time // 60000) % 60
            hours = (self.stopwatch_time // 3600000)
            self.stopwatch_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}")
            self.root.after(10, self.update_stopwatch)

# Run the App
root = tk.Tk()
app = AlarmStopwatchApp(root)
root.mainloop()
