import pandas as pd
import requests
import threading
import time
 

BASE_URL = "http://127.0.0.1:8000/api/sensor-readings/"


TOOLS = {
    "01_M01": {
        "csv": "data/raw/train/01_M01_DC_train.csv"
    },
    "01_M02": {
        "csv": "data/raw/train/01_M02_DC_train.csv"
    },
    "02_M01": {
        "csv": "data/raw/train/02_M01_DC_train.csv"
    },
    "02_M02": {
        "csv": "data/raw/train/02_M02_DC_train.csv"
    }
}



def simulate_tool(tool_name, csv_path):

    print(f"Starting {tool_name}")

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():

        payload = {
            "tool_id": tool_name,
            "timestamp": row["time"],
            "ion_gauge_pressure": row["IONGAUGEPRESSURE"],
            "flowcool_pressure": row["FLOWCOOLPRESSURE"],
            "flowcool_flowrate": row["FLOWCOOLFLOWRATE"]
        }

        try:

            response = requests.post(
                BASE_URL,
                json=payload,
                timeout=5
            )

            print(
                f"{tool_name}: {response.status_code} | {response.text}"
            )

        except Exception as e:

            print(
                f"{tool_name}: ERROR -> {e}"
            )

        time.sleep(0.1)


threads = []

for tool_name, config in TOOLS.items():

    thread = threading.Thread(
        target=simulate_tool,
            args=(
                tool_name,
                config["csv"]
            )
    )

    thread.start()

    threads.append(thread)


for thread in threads:
    thread.join()


print("All simulators finished.")