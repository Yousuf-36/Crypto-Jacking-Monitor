import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os
import sys

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.preprocessor import load_and_combine_data

# Load & prepare data
df = load_and_combine_data()
df.drop(columns=["timestamp"], inplace=True)  # Drop timestamp, it's not useful

# Split features & labels
X = df.drop("label", axis=1)
y = df["label"].map({"normal": 0, "malicious": 1})  # Encode labels

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("🔍 Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "crypto_model.pkl"))
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
print(f"\n✅ Model saved to {model_path}")
