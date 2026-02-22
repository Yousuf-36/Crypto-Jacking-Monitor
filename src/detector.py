# import psutil
# import time
# import joblib
# import numpy as np
# import os
# import psutil
# # import gputil


# # Load model
# model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "crypto_model.pkl"))
# model = joblib.load(model_path)

# def count_browser_processes():
#     browsers = ['chrome', 'firefox', 'msedge', 'brave', 'opera']
#     count = 0
#     for proc in psutil.process_iter(['name']):
#         try:
#             if proc.info['name'] and any(b in proc.info['name'].lower() for b in browsers):
#                 count += 1
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#     return count

# def extract_features():
#     cpu_percent = psutil.cpu_percent(interval=1)
#     cpu_freq = psutil.cpu_freq().current
#     cpu_count = psutil.cpu_count()
#     load_avg = sum(psutil.getloadavg()) / 3 if hasattr(psutil, "getloadavg") else 0
#     browser_count = count_browser_processes()
#     return [cpu_percent, cpu_freq, cpu_count, load_avg]

# print("🚨 Real-Time Crypto-Jacking Detection Started...\n")

# try:
#     while True:
#         features = extract_features()
#         data = np.array(features).reshape(1, -1)
#         prediction = model.predict(data)[0]

#         label = "⚠️ MALICIOUS ACTIVITY DETECTED" if prediction == 1 else "✅ Normal"
#         print(f"[{time.strftime('%H:%M:%S')}] Stats: {features} → {label}")
#         time.sleep(2)

# except KeyboardInterrupt:
#     print("\n🛑 Stopped Monitoring.")



# import psutil

# # src/detector.py

# import psutil

# def get_features():
#     cpu_percent = psutil.cpu_percent(interval=1)
#     ram_percent = psutil.virtual_memory().percent
#     process_count = len(psutil.pids())

#     return {
#         "cpu": cpu_percent,
#         "ram": ram_percent,
#         "proc_count": process_count
#     }

# detector.py

import psutil
import os
import joblib
import numpy as np
import time

# Load model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "crypto_model.pkl"))
model = joblib.load(model_path)

def count_browser_processes():
    browsers = ['chrome', 'firefox', 'msedge', 'brave', 'opera']
    count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and any(b in proc.info['name'].lower() for b in browsers):
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return count

def extract_features():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current
    cpu_count = psutil.cpu_count()
    load_avg = sum(psutil.getloadavg()) / 3 if hasattr(psutil, "getloadavg") else 0
    browser_count = count_browser_processes()
    ram_percent = psutil.virtual_memory().percent  # ✅ Added as the 5th feature

    return [cpu_percent, cpu_freq, cpu_count, load_avg, browser_count, ram_percent]  # ✅ 5 features total

import psutil

def get_features():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_freq": psutil.cpu_freq().current,
        "cpu_count": psutil.cpu_count(),
        "load_avg": sum(psutil.getloadavg()) / 3 if hasattr(psutil, "getloadavg") else 0,
        "browser_count": count_browser_processes()
    }