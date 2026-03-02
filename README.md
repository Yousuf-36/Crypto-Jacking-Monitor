# 🛡️ Cryptojacking Detector

A real-time **machine learning-based cryptojacking detection system** that monitors system resources and identifies malicious cryptocurrency mining activity using a trained Random Forest classifier.

---

## 📌 What is Cryptojacking?

Cryptojacking is the unauthorized use of a victim's computer to mine cryptocurrency. It typically causes abnormal spikes in **CPU usage**, **RAM consumption**, and related system metrics — often silently running in the background via malicious scripts or browser extensions.

This tool detects such behavior in **real-time** using system telemetry and a trained ML model.

---

## 🚀 Features

- ✅ **Real-Time Monitoring** — Continuously polls system metrics every 2 seconds
- 🤖 **ML-Based Detection** — Random Forest classifier trained on labeled normal/malicious data
- 📊 **Live Dashboard** — Tkinter GUI with live-updating graphs for all tracked metrics
- 🔍 **Feature Extraction** — Tracks CPU %, CPU frequency, core count, load average, browser process count, and RAM %
- 🗂️ **Data Collection Tool** — Script to collect labeled training data under normal and malicious conditions
- 🧠 **Retrain-Ready** — Easily retrain the model with new data

---

## 🗂️ Project Structure

```
Cryptojacking_detector/
│
├── data/
│   ├── normal_data.csv          # Labeled normal system activity data
│   └── malicious_data.csv       # Labeled cryptojacking activity data
│
├── models/
│   └── crypto_model.pkl         # Trained Random Forest model (joblib)
│
├── src/
│   ├── collect_data.py          # Collects labeled system data for training
│   ├── detector.py              # Feature extraction from live system metrics
│   ├── dashboard_ui.py          # Tkinter live dashboard with real-time graphs
│   ├── train_model.py           # Trains and saves the ML model
│   ├── predict.py               # Standalone prediction script
│   ├── stress_cpu.py            # CPU stress script to simulate malicious load
│   └── ui_detector.py           # Alternative UI-based detector
│
├── utils/
│   └── preprocessor.py          # Loads and combines normal + malicious datasets
│
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

---

## 🧠 ML Model Details

| Property        | Value                            |
|-----------------|----------------------------------|
| Algorithm       | Random Forest Classifier         |
| Library         | scikit-learn                     |
| Features Used   | CPU %, CPU Freq (MHz), CPU Cores, Load Avg, Browser Process Count |
| Labels          | `normal` → 0, `malicious` → 1   |
| Train/Test Split| 80% / 20%                        |
| Model File      | `models/crypto_model.pkl`        |

---

## 📊 Monitored Features

| Feature              | Description                                      |
|----------------------|--------------------------------------------------|
| `cpu_percent`        | Current CPU utilization (%)                      |
| `cpu_freq`           | Current CPU clock frequency (MHz)                |
| `cpu_count`          | Number of logical CPU cores                      |
| `load_avg`           | Average system load (1-min avg)                  |
| `browser_count`      | Number of active browser processes               |
| `ram_percent`        | RAM usage percentage (displayed only)            |

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone git@github.com:Yousuf-36/CJM.git
cd CJM
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Launch the Real-Time Dashboard
```bash
cd src
python dashboard_ui.py
```
The dashboard will open a GUI window showing:
- System status: **✅ Normal** or **⚠️ Crypto-Jacking Detected**
- Live metric values (CPU, Frequency, Cores, Load, Browsers, RAM)
- 6 real-time scrolling graphs

---

### Collect Training Data
To collect new labeled data (e.g., simulate malicious load):
```bash
cd src
python collect_data.py
```
Adjust `label` and `duration` inside the script as needed (`"normal"` or `"malicious"`).

---

### Retrain the Model
After collecting new data:
```bash
cd src
python train_model.py
```
This will output a classification report and save the updated model to `models/crypto_model.pkl`.

---

### Simulate CPU Stress (Malicious Load)
```bash
cd src
python stress_cpu.py
```
Use this to generate malicious-like CPU activity for testing the detector.

---

## 📦 Dependencies

```
psutil
scikit-learn
pandas
numpy
joblib
matplotlib
tkinter (built-in with Python)
```

Install all via:
```bash
pip install -r requirements.txt
```

---

## 🖼️ Dashboard Preview

> The dashboard provides a dark-themed real-time monitoring interface with 6 live graphs:
> - CPU Usage (%)
> - CPU Frequency (MHz)
> - CPU Core Count
> - Load Average
> - Browser Process Count
> - RAM Usage (%)

Status indicator changes color:
- 🟢 **Green** → Normal activity
- 🔴 **Red** → Cryptojacking detected

---

## 🔄 Workflow

```
Collect Data  →  Preprocess  →  Train Model  →  Run Dashboard
(collect_data.py) (preprocessor.py) (train_model.py) (dashboard_ui.py)
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for:
- Better feature engineering
- New detection algorithms
- Improved UI/UX
- Cross-platform support

---


## 👤 Author

**Yousuf** — [@Yousuf-36](https://github.com/Yousuf-36)
