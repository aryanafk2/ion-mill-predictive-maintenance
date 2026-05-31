import pandas as pd
import joblib

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
    "ACTUALROTATIONANGLE"
]


MACHINES = [
    "01_M01",
    "01_M02",
    "02_M01",
    "02_M02"
]


all_dfs = []

print("Loading datasets...")

for machine in MACHINES:

    print(f"Loading {machine}")

    sensor_df = pd.read_csv(
        f"data/raw/train/{machine}_DC_train.csv",
        usecols=["time"] + FEATURES
    )

    ttf_df = pd.read_csv(
        f"data/raw/train/train_ttf/{machine}_DC_train.csv",
        usecols=["time", TARGET]
    )

    merged = sensor_df.merge(
        ttf_df,
        on="time"
    )

    merged = merged.dropna(
        subset=[TARGET]
    )

    all_dfs.append(
        merged
    )


print("\nCombining datasets...")

df = pd.concat(
    all_dfs,
    ignore_index=True
)

print("\nFinal Dataset Shape:")
print(df.shape)

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
print("TTF V3B RESULTS")
print("================================")
print("MAE:", mae)
print("================================")

joblib.dump(
    model,
    "backend/ml/ttf_model_v3_4machines.pkl"
)

print("\nModel saved:")
print("backend/ml/ttf_model_v3_4machines.pkl")