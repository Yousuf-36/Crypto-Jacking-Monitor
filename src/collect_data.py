import psutil
import time
import csv
import os
import datetime
import webbrowser
import subprocess

from detector import get_features

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

def count_browser_processes():
    browser_keywords = ["chrome", "firefox", "msedge", "opera", "brave", "safari"]
    count = 0
    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info["name"].lower()
            if any(browser in name for browser in browser_keywords):
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return count

def collect_data(label="normal", duration=60):
    filename = os.path.join(DATA_DIR, f"{label}_data.csv")
    fieldnames = [
        "timestamp", "cpu_percent", "cpu_freq", "cpu_count", "load_avg",
        "browser_count", "label"
    ]
    end_time = time.time() + duration
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        while time.time() < end_time:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq().current
            cpu_count = psutil.cpu_count()
            load_avg = sum(os.getloadavg()) / 3 if hasattr(os, "getloadavg") else 0
            browser_count = count_browser_processes()

            writer.writerow({
                "timestamp": datetime.datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "cpu_freq": cpu_freq,
                "cpu_count": cpu_count,
                "load_avg": load_avg,
                "browser_count": browser_count,
                "label": label
            })


def collect_data(label="normal", duration=60):
    import csv, time

    filename = f"../data/{label}_data.csv"
    end_time = time.time() + duration

    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["cpu", "ram", "proc_count", "gpu", "label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while time.time() < end_time:
            data = get_features()
            data["label"] = label
            writer.writerow(data)
            time.sleep(2)

if __name__ == "__main__":
    collect_data(label="malicious", duration=60)


