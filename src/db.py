"""
db.py
-----
Database bootstrap for the crime dashboard.

Creates a single in-memory DuckDB connection with a ``crimes`` view pointing
at the processed parquet file, then exposes startup metadata constants used
throughout the app.

Kept separate from app.py so the connection and metadata can be imported by
any future module without triggering a Shiny server reload.
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PARQUET_PATH = BASE_DIR / "data" / "processed" / "crime.parquet"

# ---------------------------------------------------------------------------
# Single persistent read-only-style connection.
# DuckDB queries the parquet file directly — no full in-memory load required.
# ---------------------------------------------------------------------------

con = duckdb.connect(database=":memory:", read_only=False)
con.execute(f"CREATE VIEW crimes AS SELECT * FROM read_parquet('{PARQUET_PATH}')")

# ---------------------------------------------------------------------------
# Startup metadata — cheap column-statistics queries, no full scan
# ---------------------------------------------------------------------------

_meta = con.execute(
    "SELECT MIN(year) AS yr_min, MAX(year) AS yr_max FROM crimes"
).fetchone()

YEAR_MIN: int = int(_meta[0])
YEAR_MAX: int = int(_meta[1])

CITY_CHOICES: list[str] = sorted(
    row[0]
    for row in con.execute(
        "SELECT DISTINCT department_name FROM crimes ORDER BY department_name"
    ).fetchall()
)

# ---------------------------------------------------------------------------
# QueryChat DataFrame — loaded once at startup, used only by the AI tab.
# Isolated here so the main dashboard's lazy DuckDB path is unaffected.
# ---------------------------------------------------------------------------

qc_df: pd.DataFrame = pd.read_parquet(PARQUET_PATH)
