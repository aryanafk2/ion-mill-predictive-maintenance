import pandas as pd
import joblib
import time

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


TARGET = "TTF_Flowcool leak"

FEATURES = [
    "ETCHSOURCEUSAGE",
    "ETCHAUXSOURCETIMER",
    "ETCHAUX2SOURCETIMER",
    "ETCHBEAMCURRENT",
    "FLOWCOOLPRESSURE",
    "ROTATIONSPEED",
    "ACTUALSTEPDURATION",
    "IONGAUGEPRESSURE",
    "ETCHBEAMVOLTAGE",
    "ACTUALROTATIONANGLE",
    "machine_id"
]

VALID_MACHINES = {
    "01_M01": 0,
    "01_M02": 1,
    "02_M01": 2,
    "03_M02": 3,
    "04_M01": 4,
    "04_M02": 5,
    "05_M01": 6,
    "05_M02": 7,
    "06_M01": 8,
    "06_M02": 9,
    "07_M01": 10,
    "08_M01": 11,
    "09_M01": 12,
    "10_M01": 13
}

ROWS_PER_MACHINE = 300_000

all_dfs = []

start_time = time.time()

print("Loading datasets...")

for machine, machine_id in VALID_MACHINES.items():

    print(f"\nLoading {machine}")

    sensor_df = pd.read_csv(
        f"data/raw/train/{machine}_DC_train.csv",
        nrows=ROWS_PER_MACHINE
    )

    ttf_df = pd.read_csv(
        f"data/raw/train/train_ttf/{machine}_DC_train.csv",
        nrows=ROWS_PER_MACHINE
    )

    merged = sensor_df.merge(
        ttf_df,
        on="time"
    )

    merged = merged.dropna(
        subset=[TARGET]
    )

    merged["machine_id"] = machine_id

    all_dfs.append(merged)

    print(
        f"Rows kept: {len(merged):,}"
    )

print("\nCombining datasets...")

df = pd.concat(
    all_dfs,
    ignore_index=True
)

print("\nDataset Shape:")
print(df.shape)

print("\nTarget Statistics:")
print(df[TARGET].describe())

X = df[FEATURES]
y = df[TARGET]

print("\nSplitting train/test data...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining HistGradientBoostingRegressor...")

model = HistGradientBoostingRegressor(
    max_depth=8,
    learning_rate=0.05,
    max_iter=200,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

print("\nGenerating predictions...")

predictions = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("\n================================")
print("TTF V5 RESULTS")
print("================================")
print(f"MAE: {mae:,.2f}")
print("================================")

model_path = "backend/ml/ttf_model_v5_allmachines.pkl"

joblib.dump(
    model,
    model_path
)

elapsed = time.time() - start_time

print("\nModel saved:")
print(model_path)

print(f"\nTraining Time: {elapsed/60:.2f} minutes")