import pandas as pd

from sklearn.ensemble import RandomForestRegressor

print("Loading datasets...")

sensor_df = pd.read_csv(
    "data/raw/train/01_M01_DC_train.csv"
)

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
print("Rows after dropping NaNs:")
print(df.shape)

feature_columns = [
    "IONGAUGEPRESSURE",
    "ETCHBEAMVOLTAGE",
    "ETCHBEAMCURRENT",
    "ETCHSUPPRESSORVOLTAGE",
    "ETCHSUPPRESSORCURRENT",
    "FLOWCOOLFLOWRATE",
    "FLOWCOOLPRESSURE",
    "ETCHGASCHANNEL1READBACK",
    "ETCHPBNGASREADBACK",
    "FIXTURETILTANGLE",
    "ROTATIONSPEED",
    "ACTUALROTATIONANGLE",
    "ETCHSOURCEUSAGE",
    "ETCHAUXSOURCETIMER",
    "ETCHAUX2SOURCETIMER",
    "ACTUALSTEPDURATION"
]

X = df[feature_columns]
y = df[TARGET]

print("Training feature analysis model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
print("\nTarget Statistics")
print(y.describe())

print("\nNaN Count")
print(y.isna().sum())
print("\nShapes")
print("Sensor:", sensor_df.shape)
print("TTF:", ttf_df.shape)

print("\nDuplicate times")
print(
    "Sensor duplicates:",
    sensor_df["time"].duplicated().sum()
)

print(
    "TTF duplicates:",
    ttf_df["time"].duplicated().sum()
)
model.fit(X, y)

importance_df = pd.DataFrame({
    "feature": feature_columns,
    "importance": model.feature_importances_
})

importance_df = (
    importance_df
    .sort_values(
        by="importance",
        ascending=False
    )
)

print("\nFeature Importance Ranking\n")
print(importance_df)

print("\nTop 10 Features\n")
print(
    importance_df.head(10)
)