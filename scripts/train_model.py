from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
csv_path = BASE_DIR / "data" / "raw" / "train" / "01_M01_DC_train.csv"

print(f"Loading data from: {csv_path}")

# Load dataset
df = pd.read_csv(csv_path)

# Features for first model
features = [
    "IONGAUGEPRESSURE",
    "FLOWCOOLPRESSURE",
    "FLOWCOOLFLOWRATE"
]

X = df[features]

# Train model
model = IsolationForest(
    contamination=0.01,
    random_state=42
)

model.fit(X)

# Save model
model_path = BASE_DIR / "backend" / "ml" / "isolation_forest.pkl"

joblib.dump(model, model_path)

print(f"Model saved to: {model_path}")
print("Training completed successfully.")