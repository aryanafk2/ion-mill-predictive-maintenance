import numpy as np
from sklearn.ensemble import IsolationForest


model = IsolationForest(
    contamination=0.01,
    random_state=42
)


dummy_data = np.random.rand(100, 3)

model.fit(dummy_data)


def predict_anomaly(sensor_values):

    prediction = model.predict([sensor_values])

    score = model.decision_function([sensor_values])[0]

    is_anomaly = prediction[0] == -1

    return score, is_anomaly
