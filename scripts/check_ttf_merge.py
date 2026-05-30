import pandas as pd

sensor_df = pd.read_csv(
    "data/raw/train/01_M01_DC_train.csv",
    nrows=1000
)

ttf_df = pd.read_csv(
    "data/raw/train/train_ttf/01_M01_DC_train.csv",
    nrows=1000
)

print("Sensor rows:", len(sensor_df))
print("TTF rows:", len(ttf_df))

merged = sensor_df.merge(
    ttf_df,
    on="time"
)

print("Merged rows:", len(merged))

print("\nColumns:\n")
print(merged.columns.tolist())