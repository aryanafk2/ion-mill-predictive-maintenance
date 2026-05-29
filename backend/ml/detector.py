from pathlib import Path
import joblib


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "isolation_forest.pkl"

model = joblib.load(MODEL_PATH)


def predict_anomaly(sensor_values):

    prediction = model.predict([sensor_values])

    score = model.decision_function(
        [sensor_values]
    )[0]

    is_anomaly = prediction[0] == -1

    return score, 

def calculate_health_score(score):

    health = 50 + (score * 50)

    health = max(0, min(100, health))

    return round(health, 2)