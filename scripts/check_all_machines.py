import pandas as pd
from pathlib import Path

TARGET = "TTF_Flowcool leak"

train_dir = Path("data/raw/train/train_ttf")

results = []

for file in sorted(train_dir.glob("*_DC_train.csv")):

    machine = file.stem.replace("_DC_train", "")

    try:

        df = pd.read_csv(file)

        target = df[TARGET].dropna()

        results.append({
            "machine": machine,
            "count": len(target),
            "mean": target.mean() if len(target) else None,
            "median": target.median() if len(target) else None,
            "min": target.min() if len(target) else None,
            "max": target.max() if len(target) else None
        })

    except Exception as e:

        print(f"ERROR: {machine} -> {e}")

print("\n")
print("=" * 100)
print("MACHINE SUMMARY")
print("=" * 100)

for r in results:

    print(
        f"{r['machine']:10} | "
        f"count={r['count']:10} | "
        f"mean={r['mean']}"
    )

print("\n")
print("=" * 100)
print("MACHINES WITH NO LABELS")
print("=" * 100)

for r in results:

    if r["count"] == 0:

        print(r["machine"])

import pandas as pd
from pathlib import Path

TARGET = "TTF_Flowcool leak"

train_dir = Path("data/raw/train/train_ttf")

valid = []

for file in sorted(train_dir.glob("*_DC_train.csv")):

    machine = file.stem.replace("_DC_train", "")

    df = pd.read_csv(file)

    count = df[TARGET].dropna().shape[0]

    if count > 0:
        valid.append(machine)

print(valid)
print()
print("Total valid machines:", len(valid))