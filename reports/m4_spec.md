---
editor_options: 
  markdown: 
    wrap: 72
---

# Milestone 4 Specification

## Project: Crime Trends Dashboard (DSCI 532)

**Team:** Group 38\
**Dataset:** UCR Crime Data (1975-2015)\
**Technology Stack:** Shiny for Python, Altair, Matplotlib, DuckDB,
QueryChat

------------------------------------------------------------------------

## 4.1 Overview of Changes from M2

### Major Enhancements in M3 & M4

#### M3 Features (Assumed)

-   AI Explorer tab with QueryChat natural language interface
-   Interactive data table with row selection
-   AI-specific visualizations

#### M4 New Features

1.  **Enhanced KPI Dashboard**
    -   Expanded from 2 to 3 KPI cards
    -   Added "Highest Crime City" card
    -   Icon integration with color coding (red/gray/blue)
    -   Improved visual hierarchy
2.  **Performance Optimization**
    -   DuckDB integration for lazy query evaluation
    -   Parquet file format (from CSV)
    -   SQL-based filtering in database layer
3.  **Interactive Tooltips**
    -   Matplotlib hover functionality on trend plot
    -   Matplotlib hover functionality on city comparison plot
    -   Dynamic tooltip displays with exact values
4.  **Dataset-Wide Baseline**
    -   "All Cities Average" line on trend plot
    -   Always visible for context
    -   Dashed black line style
5.  **Chart Stability Fixes**
    -   UUID-based chart IDs to prevent Altair chart bleeding
    -   Vega/Vega-Lite v6 upgrade
    -   Fixed choropleth map rendering
6.  **Code Quality Improvements**
    -   Modularized state lookup code (`state.py`)
    -   Separated constants and helper functions
    -   Improved code organization
7.  **UX Improvements**
    -   Default selections on app load (LA, NYC, Violent Crime)
    -   Smart reset button behavior
    -   QueryChat-driven natural filtering on AI tab

------------------------------------------------------------------------

## 4.2 Updated Job Stories

| \# | Job Story | Status | Implementation | Owner |
|-------------|-------------|-------------|--------------------|-------------|
| 1 | When I am reviewing crime patterns in a city, I want to filter the data by **city** and **year range** so I can analyze long-term trends within a specific location. | ✅ Implemented | Multi-select city filter + year range slider with DuckDB optimization | Manikanth, Lavanya, Derrick |
| 2 | When I am evaluating crime composition over time, I want to compare **violent crime types** so I can see whether categories follow similar or different patterns. | ✅ Implemented | Crime type selector updates all visualizations + dataset average baseline | Lavanya, Manikanth |
| 3 | When I want to compare places, I want to select **multiple cities** and view them side-by-side so I can identify which cities had larger increases or decreases during specific periods. | ✅ Implemented | Multi-city selection with trend plot, bar chart, and color-coded comparisons | Diana, Lavanya |
| 4 | When I need historical context for decision-making, I want to identify the **peak crime year** for a selected city so I can contextualize policy changes and interventions around those time periods. | ✅ Implemented | Peak Crime Year KPI card with red styling and trend-up icon | Lavanya, Manikanth |
| 5 | **[NEW M4]** When I am analyzing crime hotspots, I want to see which city has the **highest crime rate** for my selected metric so I can prioritize resource allocation. | ✅ Implemented | "Highest Crime City" KPI card with building icon and rate display | Manikanth |
| 6 | **[NEW M4]** When I want precise values from visualizations, I want to **hover over charts** to see exact numbers so I can cite specific data points. | ✅ Implemented | Matplotlib hover tooltips on trend and comparison plots | Manikanth |
| 7 | **[NEW M4]** When comparing city trends, I want to see the **overall average** as a baseline so I can understand if a city is above or below typical rates. | ✅ Implemented | Dashed black "All Cities Average" line on trend plot | Manikanth |
| 8 | **[NEW M3]** When I want to explore crime data using natural language, I want to **ask questions** and get filtered results so I can discover insights without manual filtering. | ✅ Implemented | QueryChat integration in AI Explorer tab | Diana |
| 9 | **[NEW M3]** When I see an interesting city in filtered results, I want to **click on it** to focus all charts on that city so I can drill down into specific locations. | ✅ Implemented | Row-click selection with dynamic chart updates | Derrick |

------------------------------------------------------------------------

## 4.3 Component Inventory

### Crime Dashboard Tab

| ID | Type | Shiny Widget/Renderer | Depends On | Job Story | Owner | M4 Changes |
|----------|----------|-------------|----------|----------|----------|----------|
| `city` | Input | `ui.input_selectize()` | — | #1, #3 | Mani | Added default: ["Los Angeles", "New York City"] |
| `year_range` | Input | `ui.input_slider()` | — | #1 | Lavanya | — |
| `crime_type` | Input | `ui.input_select()` | — | #2 | Mani | Added default: "Violent Crime" |
| `map_year` | Input | `ui.input_slider()` | — | Map visualization | Mani | — |
| `reset` | Input | `ui.input_action_button()` | — | #1, #2, #3 | Mani | Resets to defaults (not empty) |
| `filtered_df` | Reactive | `@reactive.calc` | `city`, `year_range` | #1-#4 | Lavanya | **M4: DuckDB SQL queries** |
| `selected_column` | Reactive | `@reactive.calc` | `crime_type` | #2 | Mani | — |
| `peak_year` | Output | `@render.ui` | `filtered_df`, `selected_column` | #4 | Mani | **M4: Red color + arrow icon** |
| `highest_crime_city` | Output | `@render.ui` | `filtered_df`, `selected_column` | **#5 [NEW]** | Mani | **M4: New KPI card** |
| `crime_rate` | Output | `@render.ui` | `filtered_df`, `selected_column` | #1, #2 | Mani | **M4: Blue color + chart icon** |
| `trend_plot` | Output | `@render.plot` | `filtered_df`, `selected_column` | #1, #2, #3, #7 | Mani | **M4: Dataset avg line + hover** |
| `trend_tooltip` | Output | `@render.ui` | `trend_plot_hover` | **#6 [NEW]** | Mani | **M4: New tooltip display** |
| `city_comparison_plot` | Output | `@render.plot` | `filtered_df`, `selected_column` | #3 | Mani | **M4: Added hover support** |
| `city_tooltip` | Output | `@render.ui` | `city_comparison_plot_hover` | **#6 [NEW]** | Mani | **M4: New tooltip display** |
| `choropleth_map` | Output | `@render.ui` | `map_year`, `crime_type` | Geographic context | Mani | **M4: UUID fix + state aggregation** |

### AI Explorer Tab

| ID | Type | Shiny Widget/Renderer | Depends On | Job Story | Owner | Notes |
|----------|----------|--------------|----------|----------|----------|----------|
| `qc` | Config | `QueryChat()` | Parquet data | #8 | Team | M3 feature |
| `ai_row_count` | Output | `@render.ui` | `ai_clicked_df` | Data summary | Diana | M3 feature |
| `ai_city_count` | Output | `@render.ui` | `ai_clicked_df` | Data summary | Derrick | M3 feature |
| `ai_selected_city` | Reactive | `@reactive.calc` | `ai_data_table.cell_selection()` | #9 | Mani | M3 feature |
| `ai_clicked_df` | Reactive | `@reactive.calc` | `qc_vals.df()`, `ai_selected_city` | #9 | Mani | M3 feature |
| `ai_selected_city_text` | Output | `@render.ui` | `ai_selected_city` | #9 | Mani | M3 feature |
| `ai_trend_chart` | Output | `@render.ui` (Altair) | `ai_clicked_df` | Visual analysis | Lavanya | **M4: UUID fix** |
| `ai_city_bar_chart` | Output | `@render.ui` (Altair) | `ai_clicked_df` | City comparison | Diana | **M4: UUID fix** |
| `ai_data_table` | Output | `@render.data_frame` | `qc_vals.df()` | Data exploration | Derrick | M3: Row selection mode |
| `ai_download` | Output | `@render.download` | `qc_vals.df()` | Data export | Derrick | M3 feature |

------------------------------------------------------------------------

## 4.4 Calculation Details

### Crime Dashboard Calculations

#### `filtered_df` (`@reactive.calc`) — Owner: Lavanya

**M4 Enhancement: DuckDB Integration** - **Depends on:** `city` (input),
`year_range` (input) - **What it does:** - Constructs parameterized SQL
query for DuckDB - Filters crimes view by year range and selected
cities - Returns only filtered rows as DataFrame (lazy evaluation) -
Handles empty city selection (returns all cities) - **Performance:**
Only fetches needed rows from Parquet file - **Consumed by:** All
dashboard outputs

``` python
# M4 Implementation
@reactive.calc
def filtered_df() -> pd.DataFrame:
    start, end = input.year_range()
    cities = list(input.city())
    
    if cities:
        placeholders = ", ".join("?" * len(cities))
        query = f"""
            SELECT * FROM crimes
            WHERE year BETWEEN ? AND ?
              AND department_name IN ({placeholders})
        """
        params = [start, end] + cities
    else:
        query = "SELECT * FROM crimes WHERE year BETWEEN ? AND ?"
        params = [start, end]
    
    return con.execute(query, params).df()
```

#### `selected_column` (`@reactive.calc`) — Owner: Mani

-   **Depends on:** `crime_type` (input)
-   **What it does:** Maps user-friendly crime type names to column
    names in dataset
-   **Returns:** Column name string or None
-   **Consumed by:** All KPI and plot outputs

#### `peak_year` (`@render.ui`) — Owner: Lavanya

**M4 Enhancement: Styling** - **Depends on:** `filtered_df`,
`selected_column` - **What it does:** - Finds row with maximum crime
rate - Extracts year from that row - **M4:** Returns styled h3 with red
color - **Output:** Year as red bold text

#### `highest_crime_city` (`@render.ui`) — Owner: Mani

**M4 New Feature** - **Depends on:** `filtered_df`, `selected_column` -
**What it does:** - Finds row with maximum crime rate - Extracts city
name and rate value - Returns city name (h4) + rate value (smaller
text) - **Output:** City name with rate per 100k

#### `crime_rate` (`@render.ui`) — Owner: Diana

**M4 Enhancement: Styling** - **Depends on:** `filtered_df`,
`selected_column` - **What it does:** - Calculates mean of selected
crime column - Formats to 1 decimal place - **M4:** Returns styled h3
with blue color - **Output:** Average rate as blue bold text

#### `trend_plot` (`@render.plot`) — Owner: Lavanya

**M4 Enhancements: Dataset Average + Hover** - **Depends on:**
`filtered_df`, `selected_column`, `year_range` - **What it does:** 1.
Computes dataset-wide average via DuckDB SQL 2. Plots dashed black line
(All Cities Average) 3. Plots colored lines for selected cities 4.
Handles empty selection (shows only average) 5. **M4:** Enables hover
parameter - **Styling:** - Average: Black dashed, linewidth=2,
alpha=0.7, zorder=1 - Cities: Colored solid, linewidth=1.5, zorder=2 -
**Output:** Matplotlib figure with hover support

``` python
# M4 Dataset Average Query
dataset_avg = con.execute(f"""
    SELECT year, AVG("{col}") as avg_rate
    FROM crimes
    WHERE year BETWEEN ? AND ?
      AND "{col}" IS NOT NULL
    GROUP BY year
    ORDER BY year
""", [start, end]).df()
```

#### `trend_tooltip` (`@render.ui`) — Owner: Diana

**M4 New Feature** - **Depends on:** `trend_plot_hover()`,
`filtered_df`, `selected_column` - **What it does:** - Reads hover
coordinates from plot - Rounds x-coordinate to nearest year - Filters
data to hovered year - Displays city names and rates - **Output:**
Formatted text showing "Year YYYY: City1: 123.4 \| City2: 567.8"

#### `city_comparison_plot` (`@render.plot`) — Owner: Diana

**M4 Enhancement: Hover Support** - **Depends on:** `filtered_df`,
`selected_column` - **What it does:** - Groups by city, calculates
mean - Creates horizontal bar chart - Color-codes bars to match trend
plot - **M4:** Enables hover parameter - **Output:** Matplotlib
horizontal bar chart with hover

#### `city_tooltip` (`@render.ui`) — Owner: Diana

**M4 New Feature** - **Depends on:** `city_comparison_plot_hover()`,
`filtered_df`, `selected_column` - **What it does:** - Reads hover
y-coordinate - Maps to city index in sorted data - Displays city name
and exact rate - **Output:** "City Name: 123.4 per 100k"

#### `choropleth_map` (`@render.ui`) — Owner: Mani

**M4 Enhancements: State Aggregation + UUID** - **Depends on:**
`map_year`, `crime_type` - **What it does:** 1. Calls
`prepare_state_data_from_db()` for aggregation 2. Creates Altair layered
chart (background + choropleth) 3. **M4:** Generates unique ID for chart
4. **M4:** Replaces `id="vis"` with unique ID - **Output:** Altair HTML
with unique chart ID

------------------------------------------------------------------------

### AI Explorer Calculations

#### `ai_selected_city` (`@reactive.calc`) — Owner: Mani

-   **Depends on:** `qc_vals.df()`, `ai_data_table.cell_selection()`
-   **What it does:**
    -   Reads selected row from data table
    -   Extracts city name from that row
    -   Returns None if no selection
-   **Output:** City name string or None

#### `ai_clicked_df` (`@reactive.calc`) — Owner: Mani

-   **Depends on:** `qc_vals.df()`, `ai_selected_city()`
-   **What it does:**
    -   If city selected: filters to that city only
    -   If no city: returns all QueryChat-filtered data
    -   Enables drill-down behavior
-   **Output:** Filtered DataFrame

#### `ai_trend_chart` (`@render.ui`) — Owner: Lavanya

**M4 Enhancement: UUID Fix** - **Depends on:** `ai_clicked_df()` -
**What it does:** - Creates Altair line chart (\<=10 cities) or band
chart (\>10 cities) - **M4:** Generates unique chart ID - **M4:**
Replaces default `id="vis"` - **Output:** Altair HTML with UUID

#### `ai_city_bar_chart` (`@render.ui`) — Owner: Diana

**M4 Enhancement: UUID Fix** - **Depends on:** `ai_clicked_df()` -
**What it does:** - Groups by city, calculates mean violent crime -
Creates horizontal bar chart (top 20) - **M4:** Generates unique chart
ID - **Output:** Altair HTML with UUID

------------------------------------------------------------------------

## 4.5 Helper Functions & Modules

### `state.py` Module (M4 New)

**Owner:** Mani

Contains: - `CITY_TO_STATE`: Dictionary mapping city names to state
names - `STATE_FIPS`: Dictionary mapping state names to FIPS codes -
`CRIME_METRIC_MAP`: Maps UI labels to column names -
`prepare_state_data_from_db()`: Function to aggregate city data to state
level

**Purpose:** Modularize lookup tables and state aggregation logic

``` python
def prepare_state_data_from_db(
    conn: duckdb.DuckDBPyConnection,
    year: int,
    metric: str,
) -> pd.DataFrame:
    """
    Aggregate city crime data to state level.
    Returns DataFrame with columns: id, state_name, crime_rate, num_cities
    """
```

------------------------------------------------------------------------

## 4.6 Technology Stack Updates

### M4 Technology Changes

| Component | M2 | M4 | Reason |
|-------------------------|---------------|---------------|------------------|
| Database | CSV file reading | DuckDB + Parquet | Performance (lazy queries) |
| Vega/Vega-Lite | v5 | v6 | Compatibility fix |
| Chart IDs | Default `id="vis"` | UUID-based | Prevent bleeding |
| Data loading | `pd.read_csv()` | `con.execute().df()` | Query optimization |

### Dependencies Added in M4

-   `duckdb` - SQL database engine
-   `uuid` - Unique chart IDs

------------------------------------------------------------------------

## 4.7 Dependency Graph

``` mermaid
flowchart TD
    %% CRIME DASHBOARD TAB
    subgraph Crime Dashboard
        %% Inputs
        CITY[/city input/]
        YEAR[/year_range input/]
        CRIME[/crime_type input/]
        MAP_YEAR[/map_year input/]
        RESET[/reset button/]

        %% Reactive calcs
        FILTERED{{filtered_df<br/>DuckDB SQL}}
        SELECTED{{selected_column}}

        %% Outputs
        PEAK([peak_year<br/>RED + ICON])
        HIGHEST([highest_crime_city<br/>NEW M4])
        RATE([crime_rate<br/>BLUE + ICON])
        TREND([trend_plot<br/>+ dataset avg])
        TREND_TIP([trend_tooltip<br/>NEW M4])
        COMPARE([city_comparison_plot])
        COMPARE_TIP([city_tooltip<br/>NEW M4])
        MAP([choropleth_map<br/>+ UUID])

        %% Connections
        CITY --> FILTERED
        YEAR --> FILTERED
        CRIME --> SELECTED
        RESET --> CITY
        RESET --> YEAR
        RESET --> CRIME

        FILTERED --> PEAK
        FILTERED --> HIGHEST
        FILTERED --> RATE
        FILTERED --> TREND
        FILTERED --> COMPARE
        FILTERED --> MAP

        SELECTED --> PEAK
        SELECTED --> HIGHEST
        SELECTED --> RATE
        SELECTED --> TREND
        SELECTED --> COMPARE
        SELECTED --> MAP

        MAP_YEAR --> MAP

        TREND -.hover.-> TREND_TIP
        COMPARE -.hover.-> COMPARE_TIP
        FILTERED --> TREND_TIP
        FILTERED --> COMPARE_TIP
        SELECTED --> TREND_TIP
        SELECTED --> COMPARE_TIP
    end

    %% AI EXPLORER TAB
    subgraph AI Explorer
        %% QueryChat
        QC[QueryChat UI]
        QC_VALS{{qc_vals.df}}

        %% Row selection
        TABLE_SEL{{ai_data_table<br/>cell_selection}}
        SEL_CITY{{ai_selected_city}}
        CLICKED{{ai_clicked_df}}

        %% Outputs
        ROW_KPI([ai_row_count])
        CITY_KPI([ai_city_count])
        SEL_TEXT([ai_selected_city_text])
        AI_TREND([ai_trend_chart<br/>+ UUID M4])
        AI_BAR([ai_city_bar_chart<br/>+ UUID M4])
        AI_TABLE([ai_data_table])
        DOWNLOAD([ai_download])

        %% Connections
        QC --> QC_VALS
        QC_VALS --> AI_TABLE
        AI_TABLE -.click.-> TABLE_SEL
        TABLE_SEL --> SEL_CITY
        QC_VALS --> CLICKED
        SEL_CITY --> CLICKED

        CLICKED --> ROW_KPI
        CLICKED --> CITY_KPI
        CLICKED --> AI_TREND
        CLICKED --> AI_BAR
        SEL_CITY --> SEL_TEXT
        QC_VALS --> DOWNLOAD
    end

    %% Database layer
    PARQUET[(crime.parquet)]
    DUCKDB[(DuckDB<br/>in-memory)]
    
    PARQUET --> DUCKDB
    DUCKDB --> FILTERED
    DUCKDB --> MAP

    style HIGHEST fill:#fff3cd
    style TREND_TIP fill:#fff3cd
    style COMPARE_TIP fill:#fff3cd
    style FILTERED fill:#d1ecf1
    style AI_TREND fill:#fff3cd
    style AI_BAR fill:#fff3cd
    style DUCKDB fill:#d4edda
```

**Legend:** - 🟨 Yellow: New M4 components - 🔵 Blue: Major M4
enhancements - 🟩 Green: M4 technology upgrade

------------------------------------------------------------------------

## 4.8 UI Layout Structure

### Crime Dashboard Tab

```         
┌─────────────────────────────────────────────────────────────┐
│ CRIME TRENDS (1975–2015)                                    │
├─────────────────────────────────────────────────────────────┤
│ SIDEBAR                  │ MAIN CONTENT                      │
│ ┌─────────────────────┐ │                                   │
│ │ Filters             │ │ ┌─────┬─────┬─────┐              │
│ │ • City (max 6)      │ │ │🔺Peak│🏢High│📈Avg │  ← M4: 3 KPIs│
│ │ • Year Range        │ │ └─────┴─────┴─────┘              │
│ │                     │ │                                   │
│ │ Map Controls        │ │ ┌─────────────────────────────┐  │
│ │ • Map Year          │ │ │ Trend Plot + Dataset Avg    │  │
│ │ • Crime Metric      │ │ │ (with hover tooltip) ← M4   │  │
│ │                     │ │ └─────────────────────────────┘  │
│ │ [RESET]             │ │                                   │
│ └─────────────────────┘ │ ┌──────────┬────────────────┐   │
│                          │ │Choropleth│City Comparison │   │
│                          │ │   Map    │(hover) ← M4    │   │
│                          │ └──────────┴────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### AI Explorer Tab

```         
┌─────────────────────────────────────────────────────────────┐
│ SIDEBAR: QueryChat      │ MAIN CONTENT                      │
│ ┌─────────────────────┐ │                                   │
│ │ Natural Language    │ │ ┌──────┬──────┐                  │
│ │ Query Interface     │ │ │ Rows │Cities│  ← KPIs          │
│ │                     │ │ └──────┴──────┘                  │
│ │ [Ask a question...] │ │                                   │
│ │                     │ │ ┌──────────┬──────────┐          │
│ │ Filters Panel       │ │ │ Bar Chart│Trend Chart│ ← M4:UUID│
│ └─────────────────────┘ │ └──────────┴──────────┘          │
│                          │                                   │
│                          │ ┌─────────────────────────────┐  │
│                          │ │ Selected City (from click)  │  │
│                          │ └─────────────────────────────┘  │
│                          │                                   │
│                          │ ┌─────────────────────────────┐  │
│                          │ │ Data Table (clickable rows) │  │
│                          │ │ [Download CSV]              │  │
│                          │ └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

------------------------------------------------------------------------

## 4.9 Deployment Configuration

### Posit Connect Cloud

-   **Manifest:** Auto-generated via `rsconnect-python`
-   **Python Version:** 3.11
-   **Key Files:**
    -   `src/app.py` - Main application
    -   `src/state.py` - Helper module
    -   `src/www/styles.css` - Custom CSS
    -   `data/processed/crime.parquet` - Data file
    -   `data/data_description.md` - QueryChat context
    -   `requirements.txt` - Dependencies

### Environment Variables

-   `ANTHROPIC_API_KEY` - Required for QueryChat (set in Posit Connect
    platform settings)

### Module Structure

```         
src/
├── app.py           # Main Shiny app
├── state.py         # Lookup tables & helpers (M4)
├── __init__.py      # Makes src a package (M4)
└── www/
    └── styles.css   # Custom styles
```

------------------------------------------------------------------------

## 4.10 Known Issues & Future Enhancements

### Fixed in M4

-   ✅ Chart bleeding between tabs (UUID solution)
-   ✅ Vega version mismatch (upgraded to v6)
-   ✅ Map not rendering on load (default selections)
-   ✅ Missing tooltips on matplotlib charts (hover implementation)
-   ✅ No baseline context on trends (dataset average line)
-   ✅ Performance with large dataset (DuckDB migration)
-   ✅ Module import errors on deployment (package structure)

### Potential Future Enhancements

-   Add property crime categories (burglary, theft, etc.)
-   Implement year-over-year change calculations
-   Add downloadable reports from dashboard tab
-   Implement bookmark/share functionality
-   Add more geographic visualizations (city-level map)
-   Implement data caching for faster AI tab responses

------------------------------------------------------------------------

## 4.11 Team Contributions Summary

| Team Member | M4 Contributions |
|------------------------------|------------------------------------------|
| Derrick | Default city selections, deployment configuration, testing |
| Lavanya | DuckDB migration, trend plot enhancements, dataset average line, hover tooltips |
| Mani | New highest crime city KPI, icon integration, UUID fixes, state.py module, choropleth improvements |
| Diana | KPI styling, tooltip implementations, color scheme, AI Explorer chart fixes |

------------------------------------------------------------------------

**Document Version:** 1.0\
**Last Updated:** March 17, 2026\
**Status:** Final Submission
