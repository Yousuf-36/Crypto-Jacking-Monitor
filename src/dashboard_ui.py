import tkinter as tk
from tkinter import ttk
import threading
import time
import joblib
import os
import numpy as np
from detector import extract_features  # Updated function with all relevant features
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "crypto_model.pkl"))
model = joblib.load(model_path)

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto-Jacking Detection Dashboard")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1e1e1e")

        self.cpu_data = []
        self.freq_data = []
        self.count_data = []
        self.load_data = []
        self.browser_data = []
        self.ram_data = []
        self.timestamps = []

        self.status_label = tk.Label(root, text="System Status: Initializing...", font=("Segoe UI", 16),
                                     bg="#1e1e1e", fg="white")
        self.status_label.pack(pady=10)

        self.value_frame = tk.Frame(root, bg="#1e1e1e")
        self.value_frame.pack(pady=10)

        self.cpu_val = tk.Label(self.value_frame, text="", font=("Segoe UI", 12), fg="cyan", bg="#1e1e1e")
        self.freq_val = tk.Label(self.value_frame, text="", font=("Segoe UI", 12), fg="blue", bg="#1e1e1e")
        self.count_val = tk.Label(self.value_frame, text="", font=("Segoe UI", 12), fg="purple", bg="#1e1e1e")
        self.load_val = tk.Label(self.value_frame, text="", font=("Segoe UI", 12), fg="orange", bg="#1e1e1e")
        self.browser_val = tk.Label(self.value_frame, text="", font=("Segoe UI", 12), fg="lime", bg="#1e1e1e")
        self.ram_val = tk.Label(self.value_frame, text="", font=("Segoe UI", 12), fg="magenta", bg="#1e1e1e")

        self.cpu_val.grid(row=0, column=0, padx=10)
        self.freq_val.grid(row=0, column=1, padx=10)
        self.count_val.grid(row=0, column=2, padx=10)
        self.load_val.grid(row=0, column=3, padx=10)
        self.browser_val.grid(row=0, column=4, padx=10)
        self.ram_val.grid(row=0, column=5, padx=10)

        self.figure = Figure(figsize=(10, 7), dpi=100)
        self.cpu_ax = self.figure.add_subplot(611)
        self.freq_ax = self.figure.add_subplot(612)
        self.count_ax = self.figure.add_subplot(613)
        self.load_ax = self.figure.add_subplot(614)
        self.browser_ax = self.figure.add_subplot(615)
        self.ram_ax = self.figure.add_subplot(616)

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

        self.stop_flag = False
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def monitor_loop(self):
        while not self.stop_flag:
            features = extract_features()
            cpu, freq, count, load, browser, ram = features

            # Only use the 5 features the model was trained on (exclude ram)
            model_input = [cpu, freq, count, load, browser]
            data = np.array([model_input])
            prediction = model.predict(data)[0]

            status = "✅ Normal" if prediction == 0 else "⚠️ Crypto-Jacking Detected"
            status_color = "green" if prediction == 0 else "red"
            self.status_label.config(text=f"System Status: {status}", fg=status_color)

            self.cpu_val.config(text=f"CPU: {cpu:.2f}%")
            self.freq_val.config(text=f"Freq: {freq:.2f} MHz")
            self.count_val.config(text=f"Cores: {count}")
            self.load_val.config(text=f"Load: {load:.2f}")
            self.browser_val.config(text=f"Browsers: {browser}")
            self.ram_val.config(text=f"RAM: {ram:.2f}%")

            self.cpu_data.append(cpu)
            self.freq_data.append(freq)
            self.count_data.append(count)
            self.load_data.append(load)
            self.browser_data.append(browser)
            self.ram_data.append(ram)
            self.timestamps.append(time.strftime("%H:%M:%S"))

            if len(self.cpu_data) > 20:
                self.cpu_data.pop(0)
                self.freq_data.pop(0)
                self.count_data.pop(0)
                self.load_data.pop(0)
                self.browser_data.pop(0)
                self.ram_data.pop(0)
                self.timestamps.pop(0)

            self.update_graphs()
            time.sleep(2)

    def update_graphs(self):
        self.cpu_ax.clear()
        self.freq_ax.clear()
        self.count_ax.clear()
        self.load_ax.clear()
        self.browser_ax.clear()
        self.ram_ax.clear()

        self.cpu_ax.plot(self.timestamps, self.cpu_data, label='CPU (%)', color='cyan')
        self.freq_ax.plot(self.timestamps, self.freq_data, label='CPU Freq (MHz)', color='blue')
        self.count_ax.plot(self.timestamps, self.count_data, label='CPU Cores', color='purple')
        self.load_ax.plot(self.timestamps, self.load_data, label='Load Avg', color='orange')
        self.browser_ax.plot(self.timestamps, self.browser_data, label='Browser Processes', color='lime')
        self.ram_ax.plot(self.timestamps, self.ram_data, label='RAM Usage (%)', color='magenta')

        for ax in [self.cpu_ax, self.freq_ax, self.count_ax, self.load_ax, self.browser_ax, self.ram_ax]:
            ax.set_xticks([])
            ax.legend(loc='upper right')
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_facecolor("#2e2e2e")
            ax.tick_params(colors='white')

        self.figure.tight_layout()
        self.canvas.draw()

    def on_close(self):
        self.stop_flag = True
        self.root.destroy()

if __name__ == "__main__":
    print("\n Real-Time Crypto-Jacking Detection Started...\n")
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()