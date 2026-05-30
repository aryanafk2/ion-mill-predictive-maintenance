import os
import sys
import pandas as pd
import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/sensor-readings/"

TOOL_NAME = "01_M01"

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

import django
django.setup()

from api.models import Equipment

equipment = Equipment.objects.get(
    tool_id=TOOL_NAME
)

CSV_FILE = (
    f"data/raw/train/{TOOL_NAME}_DC_train.csv"
)

df = pd.read_csv(CSV_FILE)

for _, row in df.head(300).iterrows():

    payload = {
        "equipment": equipment.id,
        "timestamp": row["time"],
        "ion_gauge_pressure": row["IONGAUGEPRESSURE"],
        "flowcool_pressure": row["FLOWCOOLPRESSURE"],
        "flowcool_flowrate": row["FLOWCOOLFLOWRATE"]
    }

    response = requests.post(
        BASE_URL,
        json=payload
    )

    print(response.status_code)

    time.sleep(0.05)