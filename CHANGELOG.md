# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [0.4.0] - 2026-03-17

### Added

- Added `scripts/convert_to_parquet.py` to convert the raw CSV dataset to Parquet format, stored in `data/processed/crime.parquet` ([#77](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/77))
- Added `duckdb` as a project dependency in `environment.yml` and `requirements.txt` ([#77](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/77))
- Added contextual helper notes under KPI metric cards to clarify interpretation and units (e.g., incidents per 100k residents) ([#81](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/81))
- Created `src/state.py` module containing `CITY_TO_STATE`, `STATE_FIPS`,`CRIME_METRIC_MAP`, and `prepare_state_data()` — extracted from `app.py` to improve maintainability and separation of concerns ([#84](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/84))
- Added New KPI card - City with highest crime rate ([#85](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/85))
- Advanced feature has been integrated which plots the `Crime Rate by City` and `Violent Crime Trend Over Time` when clicked on the dataframe row ([#97](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/97))
- Added UUID to all the altair plots so there isnt a bleeding. ([#97](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/97))
- Interactive component to maltplotlib plots. The users can view the precise metric by hovering over the bar chart or line chart. ([#85](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/85))

### Changed

- Replaced module-level `pd.read_csv()` data loading with a persistent DuckDB in-memory connection backed by the Parquet file via a `CREATE VIEW` statement ([#77](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/77))
- Replaced hardcoded `crimes_df`-derived UI boundary values (`YEAR_MIN`, `YEAR_MAX`, `CITY_CHOICES`) with lightweight DuckDB metadata queries (`MIN`, `MAX`, `DISTINCT`) that scan only column statistics rather than full rows ([#77](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/77))
- Rewired `filtered_df()` reactive calc to execute a parameterised SQL query (`WHERE year BETWEEN ? AND ?` with optional `IN (...)` for cities) against DuckDB, so all filtering happens at the database level before any data enters a DataFrame ([#77](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/77))
- Replaced `prepare_state_data()` (which received the full global DataFrame) with `prepare_state_data_from_db()`, which issues a single-year DuckDB query and pulls only the matching rows into Python for state-level aggregation ([#77](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/77))
- Moved `CITY_TO_STATE`, `STATE_FIPS`, and `CRIME_METRIC_MAP` dictionaries to module level to eliminate repeated redefinition on every render call ([#84](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/84))
- `QueryChat` (AI Explorer tab) now initialises from `pd.read_parquet()` instead of `pd.read_csv()`, keeping the AI tab functional while isolating it from the main dashboard lazy-loading path ([#84](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/84))
- Removed duplicate in-plot titles from dashboard visualizations so each chart uses the card header as the single source of title text ([#84](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/84))
- Modularised state-level map data preparation logic out of `app.py` into `state.py`; `app.py` now imports `prepare_state_data` and `CRIME_METRIC_MAP` from this module ([#84](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/84))
- Cleaned `requirements.txt` by removing ~47 transitive sub-dependencies that are installed automatically by their parent packages, leaving only direct dependencies ([#98] (https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/pull/98))
- The chatbot window size has been increased for better interface  ([#83](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/83))
- The cities `Los Angeles` and `New York` are selected on default  ([#83](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/83))
- Crime metric `Violent Crime` is selected on default ([#83](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/83))

### Fixed 

- Fixed year label formatting in the Year Range slider by disabling numeric separators/decimals for cleaner integer year display ([]())
- Added missing `duckdb` entry to `requirements.txt`, which caused a `ModuleNotFoundError` on fresh clone and was the root cause of the app failing to run after cloning ([#85](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/85))
- Chart bleeding of altair plots ([#85](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/85))
- Advanced feature was not rendering the trend line plot which has been fixed ([#85](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/85))

### Known Issues

N/A

### Release Highlight: Interactive City Exploration

The advanced feature enables users to click on any city in the data table on the "AI Explorer" page and instantly update both the Crime Rate by City and Violent Crime Trend Over Time visualizations. This creates a smooth workflow where users can move from aggregate comparisons to temporal analysis for a specific city, improving analytical depth.

- **Option chosen:** D
- **PR:** #93
- **Why this option over the others:** This option provided the strongest improvement in user interactivity and exploratory analysis, directly linking tabular and visual components for a more intuitive workflow.
- **Feature prioritization issue link:** ([#97](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/97))

### Collaboration

- **M3 retrospective:** As a group, we improved collaboration by balancing distribution of coding tasks to avoid disproportionate amounts of development being authored by a small subset of members.
- **M4:** We emphasized tighter integration across features (e.g., linking dataframe interactions to plots), improved testing of reactive behavior, and enforced more consistent practices across contributors.

### Reflection

This milestone focused on improving both performance and interactivity of the dashboard. Migrating to DuckDB and Parquet helped to optimize data access, while the integration of reactive, user-driven visual updates enhanced the overall user experience. One focal point was the importance of coordinating feature development across team members to avoid integration issues such as rendering conflicts. This was particularly important when working with shared reactive components. 

## [0.3.0] - 2026-03-08

### Added

- Implemented a querychat AI chat interface ([#54](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/54))
- Created a dataframe output component to see/download the filtered dataframe ([#54](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/54))
- Appropriated main tab visualizations for use with the querychat filtered dataframe ([#54](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/54))
- Added a prompt to remind users to select a city - "no metric selected" ([#53](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/53))

### Changed

- Aligned chart titles with card headers for consistency across all visualizations ([#53](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/53))
- Converted City Comparison bar chart from vertical to horizontal orientation to prevent x-axis labels from being cut off ([#53](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/53))

### Fixed

- Synchronized color schemes between Trend Over Time line chart and City Comparison bar chart so the same city uses the same color in both visualizations ([#53](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/53))
- Fixed the reactivity of the map with filter inputs ([#53](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/53))

### Known Issues

N/A

## [0.2.0] - 2026-02-28

### Added

- Implemented components in dashboard (issues #23-26)
- Created GIF demo and contributors section for README.md ([#27](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/27#issue-3985219934))
- Implemented reactivity structure ([#28](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/28#issue-3985222765))
- Created reactivity diagram ([#29](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/29#issue-3985225748))
- Preview and stable builds deployed (issues #30-31)
- Created component inventory in specifications ([#36](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/36#issue-3985246750))

### Changed

- Updated job stories in specifications ([#37](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/37#issue-3985248141))

### Fixed

N/A

### Known Issues

N/A

### Reflection

The Crime Dashboard successfully implements the majority of the core functionality outlined in our milestone 1 proposal. User stories 1, 3, and 4 are now fully implemented with dashboard components that allow for long-term and inter-city analysis of crime trends. Said components include an interactive map displaying local crime statistics and line plot for long-term trends, with both being filterable by location and time span. User Story 2 is not yet implemented, with comparisons across violent crime subcategories (homicide, robbery, rape, and aggravated assault) still needing to be integrated.

The current composition of the dashboard includes all components of the M1 sketch and M2 specification, only deviating with some marginal layout changes. As it stands at the end of Milestone 2, there are no notable deviations from visualization best practices, nor are there any known issues.

Overall, the dashboard holds strong alignment with user needs, providing nearly every capability we sought to include. However, it is still limited in categorical crime comparisons which will be implemented in future iterations.

## [0.1.0] - 2026-02-14

### Added

- Initial repository, app skeleton setup ([#5](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/5#issue-3929168391))
- Established a dashboard proposal ([#6](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/6#issue-3929170365))
- Sketched a prospective dashboard ([#7](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/7#issue-3929171826))
- Selected a dataset, perfomed eda ([#8](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/8#issue-3929173743))
