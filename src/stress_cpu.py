import threading
import time

def stress():
    while True:
        _ = 0
        for i in range(1000000):
            _ += i*i

threads = []

print("🚨 Simulating crypto-jacked behavior (CPU stress)...")
for i in range(8):  # Adjust based on your CPU cores
    t = threading.Thread(target=stress)
    t.start()
    threads.append(t)

# Run for 60 seconds
time.sleep(60)

print("✅ Done. Stopping stress.")
# Threads will stop when script exits
