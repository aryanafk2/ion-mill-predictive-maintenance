import pandas as pd
import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/sensor-readings/"

df = pd.read_csv("data\\raw\\train\\01_M01_DC_train.csv")


for _, row in df.iterrows():

    payload = {
        "equipment": 1,
        "timestamp": row["time"],
        "ion_gauge_pressure": row["IONGAUGEPRESSURE"],
        "flowcool_pressure": row["FLOWCOOLPRESSURE"],
        "flowcool_flowrate": row["FLOWCOOLFLOWRATE"]
    }

    response = requests.post(BASE_URL, json=payload)

    print(response.status_code)

    time.sleep(0.1)
