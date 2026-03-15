# src/utils.py

CRIME_METRIC_MAP = {
    "Violent Crime": "violent_per_100k",
    "Homicide":      "homs_per_100k",
    "Rape":          "rape_per_100k",
    "Robbery":       "rob_per_100k",
    "Aggravated Assault": "agg_ass_per_100k",
}

def get_crime_column(crime_type: str) -> str | None:
    """Return the DataFrame column name for a given crime type label.
    Returns None if crime_type is 'None' or unrecognized."""
    if crime_type == "None":
        return None
    return CRIME_METRIC_MAP.get(crime_type)