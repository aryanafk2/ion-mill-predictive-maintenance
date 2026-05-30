from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "ttf_model.pkl"
)

def predict_ttf(sensor_values):
    return float(
        model.predict([sensor_values])[0]
    )