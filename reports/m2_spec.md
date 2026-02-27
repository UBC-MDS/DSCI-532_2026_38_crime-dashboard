# Milestone 2 Specification

## 2.1 Updated Job Stories


| # | Job Story | Status | Notes |
|---|----------|--------|------|
| 1 | When I am reviewing crime patterns in a city, I want to filter the data by **city** and **year range** so I can analyze long-term trends within a specific location. | ✅ Implemented | Implemented in M2 via the Filters panel (city selector + year range slider) and reflected in the trend plot, KPIs, and map. |
| 2 | When I am evaluating crime composition over time, I want to compare **violent vs property** crime trends (and/or their subcategories) so I can see whether categories follow similar or different patterns. | ✅ Implemented | Implemented in M2 via the crime type selector; updates the time-series plot and the city comparison chart (and any KPI metrics tied to the selected type). |
| 3 | When I want to compare places, I want to select **multiple cities** and view them side-by-side so I can identify which cities had larger increases or decreases during specific periods. | ✅ Implemented | Implemented in M2 via multi-select city filtering; comparison is supported through multi-line trends and a city comparison bar chart, with the map providing geographic context. |
| 4 | When I need historical context for decision-making, I want to identify the **peak crime year** for a selected city (and selected crime metric) so I can contextualize policy changes and interventions around those time periods. | ✅ Implemented | Implemented in M2 as a KPI/value box showing peak year (and peak rate/value) computed from the filtered data for the selected city/cities and crime type. |


### 2.2 Component Inventory
| ID | Type | Shiny widget / renderer | Depends on | Job story | Owner |
|----|------|--------------------------|------------|-----------|--------|
| `city` | Input | `ui.input_selectize()` (multi-select cities) | — | #1, #3 | Derrick |
| `year_range` | Input | `ui.input_slider()` (1975–2015 range slider) | — | #1 | Derrick |
| `crime_type` | Input | `ui.input_select()` (violent/property) | — | #2 | Mani |
| `reset` | Input | `ui.input_action_button()` (reset filters) | — | #1, #2, #3 | Mani |
| `filtered_df` | Reactive calc | `@reactive.calc` | `city`, `year_range`, `crime_type` | #1, #2, #3, #4 | Lavanya |
| `peak_stats` | Reactive calc | `@reactive.calc` | `filtered_df` | #4 | Lavanya |
| `kpi_stats` | Reactive calc | `@reactive.calc` | `filtered_df` | #1, #2 | Diana |
| `comparison_df` | Reactive calc | `@reactive.calc` | `filtered_df` | #3 | Diana |
| `map_df` | Reactive calc | `@reactive.calc` | `filtered_df` | #3 | Mani |
| `out_peak_year` | Output | `@render.ui` (value box / text) | `peak_stats` | #4 | Lavanya |
| `out_crime_rate` | Output | `@render.ui` (value box / text) | `kpi_stats` | #1, #2 | Diana |
| `out_trend_plot` | Output | `@render.plot` (or altair renderer) | `filtered_df` | #1, #2, #3 | Lavanya |
| `out_map` | Output | `@render.plot` | `map_df` | #3 | Mani |
| `out_city_comparison` | Output | `@render.plot` | `comparison_df` | #3 | Derrick |

### 2.3 Reactivity Diagram 
flowchart TD
  %% Inputs (these match src/app.py)
  C[/city/] --> F{{filtered_df}}
  Y[/year_range/] --> F
  T[/crime_type/] --> F
  R[/reset/] --> RE{{reset_effect}}

  %% Reactive calcs
  F --> PK{{peak_stats}}
  F --> KPI{{kpi_stats}}
  F --> CMP{{comparison_df}}
  F --> MAP{{map_df}}

  %% Outputs
  PK --> O1([out_peak_year])
  KPI --> O2([out_crime_rate])
  F --> O3([out_trend_plot])
  MAP --> O4([out_map])
  CMP --> O5([out_city_comparison])

  %% Reset effect (optional logic)
  RE --> C
  RE --> Y
  RE --> T
  
  
  ## 2.4 Calculation Details

### `filtered_df`  (`@reactive.calc`)  — Owner: Lavanya
- **Depends on inputs:** `city`, `year_range`, `crime_type`
- **What it does:** Loads the base dataset and filters rows to the selected city/cities and year range. Chooses the correct crime metric column based on `crime_type` (e.g., violent vs property; rate per 100k vs counts as defined in the app).
- **Consumed by outputs:** `out_trend_plot`, and indirectly supports `out_peak_year`, `out_crime_rate`, `out_city_comparison`, `out_map` through downstream calcs.

### `peak_stats`  (`@reactive.calc`)  — Owner: Lavanya
- **Depends on:** `filtered_df`
- **What it does:** Computes peak crime information from the filtered data (e.g., identifies the year with the maximum selected crime metric for the selected city/cities, and returns the peak year and peak value).
- **Consumed by outputs:** `out_peak_year` (and can also be used for an optional “peak value” KPI if added later).

### `kpi_stats`  (`@reactive.calc`)  — Owner: Diana
- **Depends on:** `filtered_df`
- **What it does:** Computes KPI values for the cards using the **most recent year in `year_range`** (right endpoint). For example, returns the selected crime metric (rate per 100k or count) for that year, for the selected city (or an aggregate if multiple cities are selected).
- **Consumed by outputs:** `out_crime_rate`.

### `comparison_df`  (`@reactive.calc`)  — Owner: Diana
- **Depends on:** `filtered_df`
- **What it does:** Creates a city-level summary for the bar chart using the **most recent year in `year_range`** (right endpoint). Produces one value per selected city for the selected crime metric.
- **Consumed by outputs:** `out_city_comparison`.

### `map_df`  (`@reactive.calc`)  — Owner: Mani
- **Depends on:** `filtered_df`
- **What it does:** Prepares data for the map view (e.g., joins filtered crime data with city coordinates and computes the mapped value for the selected crime type and year range).
- **Consumed by outputs:** `out_map`.



