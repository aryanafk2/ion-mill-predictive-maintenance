from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "ttf_model_v5_allmachines.pkl"
)


def predict_ttf(sensor_values):

    prediction = model.predict(
        [sensor_values]
    )[0]

    return float(prediction)