import tkinter as tk
from tkinter import Toplevel, Label
import threading
import time
import joblib
import os
import pandas as pd
from detector import get_features  # should return a dict with cpu, ram, proc_count, gpu

# Load model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "crypto_model.pkl"))
model = joblib.load(model_path)


class DetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto-Jacking Detector")
        self.root.geometry("360x200")
        self.root.configure(bg="#1e1e1e")

        self.status_label = tk.Label(root, text="🕵️ Monitoring system...", font=("Segoe UI", 14),
                                     bg="#1e1e1e", fg="white")
        self.status_label.pack(pady=40)

        self.prediction_label = tk.Label(root, text="", font=("Segoe UI", 12),
                                         bg="#1e1e1e", fg="gray")
        self.prediction_label.pack()

        self.stop_flag = False
        threading.Thread(target=self.predict_and_update, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def predict_and_update(self):
        while not self.stop_flag:
            features_dict = get_features()
            X = pd.DataFrame([features_dict])[model.feature_names_in_]
            prediction = model.predict(X)[0]

            if prediction == 1:
                self.status_label.config(text="⚠️ Crypto-Jacking Detected!", fg="red")
                self.prediction_label.config(text="Malicious behavior identified.")
                self.root.after(0, lambda: self.show_custom_popup(features_dict, prediction))
            else:
                self.status_label.config(text="✅ System Safe", fg="green")
                self.prediction_label.config(text="No crypto-jacking detected.")

            time.sleep(5)

    def show_custom_popup(self, data, prediction):
        popup = tk.Toplevel(self.root)
        popup.title("⚠️ Crypto-Jacking Alert")
        popup.geometry("350x200")
        popup.configure(bg="#1e1e1e")

        popup.lift()
        popup.attributes("-topmost", True)
        popup.focus_force()

        status = "🚨 MALICIOUS ACTIVITY DETECTED" if prediction == 1 else "✅ NORMAL BEHAVIOR"
        status_color = "red" if prediction == 1 else "green"

        tk.Label(popup, text=status, font=("Segoe UI", 14, "bold"),
                 fg=status_color, bg="#1e1e1e").pack(pady=10)

        tk.Label(popup, text=f"CPU Usage: {data['cpu']}%", font=("Segoe UI", 11),
                 bg="#1e1e1e", fg="white").pack()

        tk.Label(popup, text=f"GPU Usage: {data['gpu']}%", font=("Segoe UI", 11),
                 bg="#1e1e1e", fg="white").pack()

        tk.Label(popup, text=f"Running Processes: {data['proc_count']}", font=("Segoe UI", 11),
                 bg="#1e1e1e", fg="white").pack()

        if 'browser_count' in data:
            tk.Label(popup, text=f"Browser Tabs Open: {data['browser_count']}", font=("Segoe UI", 11),
                     bg="#1e1e1e", fg="white").pack()

        popup.after(7000, popup.destroy)  # Auto-close after 7 seconds

    def on_close(self):
        self.stop_flag = True
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorApp(root)
    root.mainloop()
