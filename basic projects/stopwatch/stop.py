import tkinter as tk
import time


class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Stopwatch")
        self.root.geometry("500x400")
        self.root.config(bg="#1e1e2f")

        # Initialize variables
        self.start_time = 0
        self.running = False
        self.elapsed_time = 0
        self.current_action = -1  # To track the last action

        # Timer display
        self.timer_label = tk.Label(
            self.root,
            text="00:00:00.000",
            font=("Courier", 30, "bold"),
            bg="#1e1e2f",
            fg="#00ffcc",
        )
        self.timer_label.pack(pady=40)

        # Instructions label
        self.instructions_label = tk.Label(
            self.root,
            text="Slide to Start, Stop, or Reset",
            font=("Arial", 14, "italic"),
            bg="#1e1e2f",
            fg="#ffffff",
        )
        self.instructions_label.pack(pady=10)

        # Sliding controls
        self.control_slider = tk.Scale(
            self.root,
            from_=0,
            to=2,
            orient=tk.HORIZONTAL,
            length=300,
            showvalue=False,
            tickinterval=1,
            resolution=1,
            bg="#1e1e2f",
            fg="#ffffff",
            troughcolor="#00ffcc",
            sliderlength=40,
            width=20,
            font=("Arial", 12),
            command=self.slider_action,
        )
        self.control_slider.pack(pady=20)

        # Slider labels
        self.slider_labels = tk.Frame(self.root, bg="#1e1e2f")
        tk.Label(self.slider_labels, text="Start", bg="#1e1e2f", fg="#28a745", font=("Arial", 12)).pack(side=tk.LEFT, padx=60)
        tk.Label(self.slider_labels, text="Stop", bg="#1e1e2f", fg="#dc3545", font=("Arial", 12)).pack(side=tk.LEFT, padx=60)
        tk.Label(self.slider_labels, text="Reset", bg="#1e1e2f", fg="#007bff", font=("Arial", 12)).pack(side=tk.LEFT, padx=60)
        self.slider_labels.pack()

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(self.elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = (self.elapsed_time - int(self.elapsed_time)) * 1000

            time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
            self.timer_label.config(text=time_str)

            # Call update_timer every 10 milliseconds
            self.root.after(10, self.update_timer)

    def start_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False

    def reset_timer(self):
        self.running = False
        self.elapsed_time = 0
        self.timer_label.config(text="00:00:00.000")

    def slider_action(self, value):
        value = int(value)

        # If slider has been moved to the same position, ignore the action
        if value == self.current_action:
            return

        # Perform the action based on slider value
        if value == 0:  # Start
            self.start_timer()
        elif value == 1:  # Stop
            self.stop_timer()
        elif value == 2:  # Reset
            self.reset_timer()

        # Track the action but don't reset slider immediately
        self.current_action = value

    def reset_slider(self):
        """Reset the slider position only after Stop or Reset action"""
        if self.current_action == 1 or self.current_action == 2:
            self.control_slider.set(-1)


# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()
