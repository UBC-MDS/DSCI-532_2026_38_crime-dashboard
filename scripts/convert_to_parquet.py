"""
Run once from the repo root:
    python scripts/convert_to_parquet.py

Reads  : data/raw/ucr_crime_1975_2015.csv
Writes : data/processed/crime.parquet
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "ucr_crime_1975_2015.csv"
OUT_DIR  = BASE_DIR / "data" / "processed"
OUT_PATH = OUT_DIR / "crime.parquet"

OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_PATH)

# Enforce correct dtypes so DuckDB can predicate-push properly
df["year"] = df["year"].astype("int32")
df["department_name"] = df["department_name"].astype("str")

for col in [
    "violent_per_100k", "homs_per_100k",
    "rape_per_100k", "rob_per_100k", "agg_ass_per_100k",
]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("float32")

df.to_parquet(OUT_PATH, index=False, engine="pyarrow", compression="snappy")

print(f"Written {len(df):,} rows -> {OUT_PATH}")
print(f"File size: {OUT_PATH.stat().st_size / 1024:.1f} KB")
