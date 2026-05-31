import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


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

print("Removing rows with missing TTF labels...")

df = df.dropna(
    subset=[TARGET]
)

print("\nDataset Shape:")
print(df.shape)

print("\nTarget Statistics:")
print(df[TARGET].describe())

print("\nCorrelation Analysis")
print(
    df[[
        "ETCHSOURCEUSAGE",
        "ETCHAUXSOURCETIMER",
        "ETCHAUX2SOURCETIMER",
        TARGET
    ]].corr()
)


# ==========================================
# Feature Sets
# ==========================================

baseline_features = [
    "IONGAUGEPRESSURE",
    "FLOWCOOLPRESSURE",
    "FLOWCOOLFLOWRATE"
]

top3_features = [
    "ETCHSOURCEUSAGE",
    "ETCHAUXSOURCETIMER",
    "ETCHAUX2SOURCETIMER"
]

top10_features = [
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


# ==========================================
# Training Function
# ==========================================

def evaluate_model(name, features):

    print(f"\nTraining {name}...")

    X = df[features]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    print("\n==============================")
    print(name)
    print("==============================")
    print(f"Features Used: {len(features)}")
    print(f"MAE: {mae:.4f}")

    return mae


# ==========================================
# Run Experiments
# ==========================================

baseline_mae = evaluate_model(
    "Baseline Model",
    baseline_features
)

top3_mae = evaluate_model(
    "Top 3 Features Model",
    top3_features
)

top10_mae = evaluate_model(
    "Top 10 Features Model",
    top10_features
)


# ==========================================
# Final Results
# ==========================================

print("\n========================================")
print("FINAL RESULTS")
print("========================================")

print(f"Baseline Model MAE : {baseline_mae:.4f}")
print(f"Top 3 Model MAE    : {top3_mae:.4f}")
print(f"Top 10 Model MAE   : {top10_mae:.4f}")

best_mae = min(
    baseline_mae,
    top3_mae,
    top10_mae
)

if best_mae == baseline_mae:
    best_model = "Baseline Model"
elif best_mae == top3_mae:
    best_model = "Top 3 Features Model"
else:
    best_model = "Top 10 Features Model"

print(f"\nBest Model: {best_model}")
print("========================================")