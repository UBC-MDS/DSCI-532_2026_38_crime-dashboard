# tests/test_utils.py
from src.utils import get_crime_column

# Verifies that a valid crime type maps to its correct column name,
# since an incorrect mapping would silently show wrong KPI and chart data.
def test_get_crime_column_valid():
    assert get_crime_column("Violent Crime") == "violent_per_100k"
    assert get_crime_column("Homicide") == "homs_per_100k"
    assert get_crime_column("Robbery") == "rob_per_100k"

# Verifies that "None" returns None so KPI cards show their placeholder message,
# since returning a wrong column name would crash the peak_year and crime_rate outputs.
def test_get_crime_column_none_string():
    assert get_crime_column("None") is None

# Verifies that an unrecognized crime type returns None rather than raising an error,
# so any future UI additions don't crash the server silently.
def test_get_crime_column_unknown():
    assert get_crime_column("Burglary") is None