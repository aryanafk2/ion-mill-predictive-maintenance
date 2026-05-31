import pandas as pd

TARGET = "TTF_Flowcool leak"

MACHINES = [
    "01_M01",
    "01_M02",
    "02_M01",
    "02_M02"
]

for machine in MACHINES:

    print("\n" + "=" * 50)
    print(machine)
    print("=" * 50)

    ttf_df = pd.read_csv(
        f"data/raw/train/train_ttf/{machine}_DC_train.csv"
    )

    target = ttf_df[TARGET].dropna()

    print(target.describe())

    print("\nMin:", target.min())
    print("Max:", target.max())
    print("Mean:", target.mean())
    print("Median:", target.median())