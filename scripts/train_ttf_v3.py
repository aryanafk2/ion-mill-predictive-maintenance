import pandas as pd
import joblib

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


print("Loading sensor data...")

sensor_df = pd.read_csv(
    "data/raw/train/01_M01_DC_train.csv"
)

print("Loading TTF data...")

ttf_df = pd.read_csv(
    "data/raw/train/train_ttf/01_M01_DC_train.csv"
)

print("Merging datasets...")

df = sensor_df.merge(
    ttf_df,
    on="time"
)

TARGET = "TTF_Flowcool leak"

df = df.dropna(
    subset=[TARGET]
)

features = [
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

print("\nDataset Shape:")
print(df.shape)

X = df[features]
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
print("TTF V3 RESULTS")
print("================================")
print("MAE:", mae)
print("================================")

joblib.dump(
    model,
    "backend/ml/ttf_model_v3.pkl"
)

print("\nModel saved:")
print("backend/ml/ttf_model_v3.pkl")