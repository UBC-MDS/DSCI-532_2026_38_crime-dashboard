"""
geo_lookup.py
-------------
Static lookup tables and helpers for mapping city-level crime data to U.S.
states for the choropleth map.

Separated from app.py per the modularisation feedback (M2 code-quality sprint).
"""

from __future__ import annotations

import pandas as pd
import duckdb


# ---------------------------------------------------------------------------
# City → State name
# ---------------------------------------------------------------------------

CITY_TO_STATE: dict[str, str | None] = {
    'Albuquerque, N.M.': 'New Mexico',
    'Arlington, Texas': 'Texas',
    'Aurora, Colo.': 'Colorado',
    'Austin, Texas': 'Texas',
    'Baltimore County, Md.': 'Maryland',
    'Buffalo, N.Y.': 'New York',
    'Charlotte-Mecklenburg, N.C.': 'North Carolina',
    'Columbus, Ohio': 'Ohio',
    'El Paso, Texas': 'Texas',
    'Fairfax County, Va.': 'Virginia',
    'Fort Worth, Texas': 'Texas',
    'Fresno, Calif.': 'California',
    'Jacksonville, Fla.': 'Florida',
    'Kansas City, Mo.': 'Missouri',
    'Long Beach, Calif.': 'California',
    'Los Angeles County, Calif.': 'California',
    'Louisville, Ky.': 'Kentucky',
    'Memphis, Tenn.': 'Tennessee',
    'Mesa, Ariz.': 'Arizona',
    'Miami-Dade County, Fla.': 'Florida',
    'Montgomery County, Md.': 'Maryland',
    'Nashville, Tenn.': 'Tennessee',
    'Nassau County, N.Y.': 'New York',
    'Newark, N.J.': 'New Jersey',
    'Oakland, Calif.': 'California',
    'Omaha, Neb.': 'Nebraska',
    'Orlando, Fla.': 'Florida',
    'Portland, Ore.': 'Oregon',
    'Prince Georges County, Md.': 'Maryland',
    "Prince George's County, Md.": 'Maryland',
    'Raleigh, N.C.': 'North Carolina',
    'Sacramento, Calif.': 'California',
    'San Diego, Calif.': 'California',
    'San Jose, Calif.': 'California',
    'St. Louis, Mo.': 'Missouri',
    'St. Paul, Minn.': 'Minnesota',
    'Suffolk County, N.Y.': 'New York',
    'Tampa, Fla.': 'Florida',
    'Tucson, Ariz.': 'Arizona',
    'Tulsa, Okla.': 'Oklahoma',
    'Virginia Beach, Va.': 'Virginia',
    'Washington, D.C.': 'District of Columbia',
    'Wichita, Kan.': 'Kansas',
    'Atlanta': 'Georgia',
    'Baltimore': 'Maryland',
    'Boston': 'Massachusetts',
    'Chicago': 'Illinois',
    'Cincinnati': 'Ohio',
    'Cleveland': 'Ohio',
    'Dallas': 'Texas',
    'Denver': 'Colorado',
    'Detroit': 'Michigan',
    'Honolulu': 'Hawaii',
    'Houston': 'Texas',
    'Indianapolis': 'Indiana',
    'Las Vegas': 'Nevada',
    'Los Angeles': 'California',
    'Miami': 'Florida',
    'Milwaukee': 'Wisconsin',
    'Minneapolis': 'Minnesota',
    'New Orleans': 'Louisiana',
    'New York City': 'New York',
    'Oklahoma City': 'Oklahoma',
    'Philadelphia': 'Pennsylvania',
    'Phoenix': 'Arizona',
    'Pittsburgh': 'Pennsylvania',
    'Salt Lake City': 'Utah',
    'San Antonio': 'Texas',
    'San Diego': 'California',
    'San Francisco': 'California',
    'San Jose': 'California',
    'Seattle': 'Washington',
    'National': None,
}


# ---------------------------------------------------------------------------
# State name → FIPS numeric id (required by Vega/Altair's US topojson)
# ---------------------------------------------------------------------------

STATE_FIPS: dict[str, int] = {
    'Alabama': 1, 'Arizona': 4, 'California': 6, 'Colorado': 8,
    'Connecticut': 9, 'District of Columbia': 11, 'Florida': 12,
    'Georgia': 13, 'Hawaii': 15, 'Illinois': 17, 'Indiana': 18,
    'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22, 'Maryland': 24,
    'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27, 'Missouri': 29,
    'Nebraska': 31, 'Nevada': 32, 'New Jersey': 34, 'New Mexico': 35,
    'New York': 36, 'North Carolina': 37, 'Ohio': 39, 'Oklahoma': 40,
    'Oregon': 41, 'Pennsylvania': 42, 'Tennessee': 47, 'Texas': 48,
    'Utah': 49, 'Virginia': 51, 'Washington': 53, 'Wisconsin': 55,
}


# ---------------------------------------------------------------------------
# UI label → parquet column name
# ---------------------------------------------------------------------------

CRIME_METRIC_MAP: dict[str, str] = {
    "Violent Crime":      "violent_per_100k",
    "Homicide":           "homs_per_100k",
    "Rape":               "rape_per_100k",
    "Robbery":            "rob_per_100k",
    "Aggravated Assault": "agg_ass_per_100k",
}


# ---------------------------------------------------------------------------
# State-level aggregation helper
# ---------------------------------------------------------------------------

_EMPTY_STATE_DF = pd.DataFrame(
    columns=["id", "state_name", "crime_rate", "num_cities"]
)


def prepare_state_data(
    conn: duckdb.DuckDBPyConnection,
    year: int,
    metric: str,
) -> pd.DataFrame:
    """
    Aggregate city-level crime data to the state level for a given year and
    crime metric.

    Filtering happens entirely inside DuckDB so only the ~35 aggregated state
    rows are transferred into Python.

    Parameters
    ----------
    conn:   Active DuckDB connection with a ``crimes`` view registered.
    year:   The year to filter on.
    metric: The parquet column name for the desired crime metric
            (use ``CRIME_METRIC_MAP`` to convert from UI labels).

    Returns
    -------
    DataFrame with columns [id, state_name, crime_rate, num_cities], where
    ``id`` is the integer FIPS code expected by the Vega US topojson.
    """
    rows = conn.execute(
        f"""
        SELECT department_name, "{metric}"
        FROM crimes
        WHERE year = ?
          AND "{metric}" IS NOT NULL
        """,
        [year],
    ).fetchall()

    if not rows:
        return _EMPTY_STATE_DF.copy()

    records = [
        {"state_name": state, "crime_rate": rate}
        for dept, rate in rows
        if (state := CITY_TO_STATE.get(dept)) is not None
    ]

    if not records:
        return _EMPTY_STATE_DF.copy()

    agg = (
        pd.DataFrame(records)
        .groupby("state_name")
        .agg(crime_rate=("crime_rate", "mean"), num_cities=("crime_rate", "count"))
        .reset_index()
    )
    agg["id"] = agg["state_name"].map(STATE_FIPS)
    agg = agg.dropna(subset=["id"])
    agg["id"] = agg["id"].astype(int)
    return agg
