## Section 1: Motivation and Purpose

> **Our role:** Data scientist consultancy firm
> **Target audience:** Public safety policy analysts and city-level decision makers (e.g., municipal public safety departments)
>
> Historical crime data contains decades of valuable information, but it is often stored in raw tabular formats that are difficult to interpret and compare. The city-level UCR dataset (1975–2015) published by The Marshall Project provides long-term crime statistics across major U.S. cities, yet extracting meaningful trends from a CSV file requires significant manual effort.
>
> Public safety analysts need to understand how violent and property crime have changed over time, identify peak periods, and compare patterns across cities. Without interactive tools, this process is slow, fragmented, and prone to oversimplification.
>
> To address this challenge, we propose building an interactive crime trends dashboard that allows policy analysts to visually explore long-term crime data. Our app will display trends over time, allow filtering by city and year range, and enable comparisons between crime categories and across multiple cities. By transforming raw data into clear visualizations, the dashboard will help decision makers identify patterns, detect anomalies, and generate evidence-based insights to inform public safety strategies.

## Section 2: Description of the Data 

**Key Variables**:

-   **Geographic/Temporal**: `department_name` (city), `year` (1975-2015), `ORI` (agency identifier)
-   **Population**: `total_pop` (city population for rate calculations)
-   **Violent Crime Totals**: `violent_crime` (sum of all violent offenses), `homs_sum` (homicides), `rape_sum`, `rob_sum` (robberies), `agg_ass_sum` (aggravated assaults)
-   **Crime Rates**: `violent_per_100k`, `homs_per_100k`, `rape_per_100k`, `rob_per_100k`, `agg_ass_per_100k` (all normalized per 100,000 population)
-   **Data Quality**: `months_reported` (indicates completeness of annual reporting)
-   **Rows in Dataset**: 2898

## Section 3: Research Questions & Usage Scenarios

### Persona
> Name: Jordan Ramirez
> Role: Public Safety Policy Analyst
> Organization: The Marshall Project (our data source reference)
> Experience Level: Mid-career analyst (say 5–7 years in criminal justice policy)
> Goals:
> - Identify long-term crime trends across U.S. cities
> - Detect structural shifts (e.g., post-1990s decline, 2008 recession era, post-2010 fluctuations)
> - Support data-driven policy recommendations
> Technical Skills:
> - Comfortable with dashboards and filtering tools
> - Familiar with UCR definitions (violent crime, property crime)
> - Limited coding ability and mostly relies on visual analytics tools
> Pain Points:
> - Raw CSV datasets are difficult to interpret quickly
> - Hard to compare cities consistently over long time spans
> - Needs evidence-based insights rather than isolated statistics

### Usage Scenario Narrative
> Jordan is a public safety policy analyst reviewing long-term crime trends using historical UCR data (1975–2015) from major U.S. cities. He wants to understand how violent and property crime rates have changed over time and whether patterns differ significantly between cities.

> When Jordan logs into the Crime Trends Dashboard, he sees:
> - An overview panel showing total crime counts by year
> - Filters for city, year range, and crime type (violent vs property crime categories from the dataset)
> - Line charts displaying trends from 1975 to 2015
> - Comparative views allowing side-by-side city analysis
> Jordan begins by selecting a single city to examine its long-term trajectory. He then adjusts the year slider to focus on specific decades (e.g., 1980s peak crime years vs post-2000 declines).

> Next, he compares two cities to see whether crime declines occurred simultaneously or at different times. He may observe that while most cities show a general decline in violent crime after the early 1990s, the magnitude and timing vary significantly.
> Using the dashboard, Jordan identifies:
> - Years with peak violent crime
> - Periods of sustained decline
> - Differences between violent and property crime trends
> - Cities that deviate from national patterns
> Based on these findings, Jordan can form hypotheses about contributing factors (e.g., policy reforms, economic shifts, demographic changes) and propose further investigation. The dashboard does not explain causation but helps him detect patterns worth deeper study.

### User Stories
> User Story 1
> As a public safety policy analyst, I want to filter crime data by city and year range so that I can analyze long-term trends within a specific location.

> User Story 2
> As a policy analyst, I want to compare violent and property crime trends so that I can understand whether different crime categories follow similar or divergent patterns over time.

> User Story 3
> As a policy analyst, I want to compare multiple cities side-by-side so that I can identify which cities experienced larger increases or decreases in crime during specific periods.

> User Story 4
> As a policy analyst, I want to identify peak crime years for each city so that I can contextualize policy changes and major interventions around those time periods.

## Section 4: Exploratory Data Analysis 
### Relevance to User Stories

This dataset directly supports our dashboard's purpose:

1.  **Long-term Trend Analysis** (User Story 1 & 4): The 41-year timeframe captures complete crime cycles, including the 1990s crime surge and subsequent decline, enabling policy analysts to identify peak years and intervention periods.

2.  **Crime Category Comparison** (User Story 2): Separate violent crime totals allow comparison between homicides, robberies, rapes, and assaults to understand whether different crime types follow similar or divergent patterns.

3.  **Multi-city Comparison** (User Story 3): With 68 major cities, analysts can compare how crime evolved differently across geographic regions, identifying outliers and testing hypotheses about policy effectiveness.

4.  **Normalized Metrics**: Pre-calculated per-100k rates account for population changes over time, ensuring fair comparisons both within cities across decades and between cities of different sizes.

To validate that our dataset supports the dashboard's user stories, we conducted an exploratory analysis focused on **User Story 4**: *"As a policy analyst, I want to identify peak crime years for each city so that I can contextualize policy changes and major interventions around those time periods."*

Our analysis examined violent crime trends across five major U.S. cities (Chicago, Los Angeles, New York, Detroit, and Philadelphia) from 1975 to 2015. The visualizations reveal several key patterns that directly enable the user story's decision-making needs:

**Visualization 1: Violent Crime Trends Over Time** (see `notebooks/eda_analysis.ipynb`)

This line chart displays violent crime rates per 100,000 population for each city across the 41-year period. The visualization demonstrates that:

-   Each city exhibits a distinct peak violent crime period, predominantly occurring in the early 1990s
-   Detroit experienced the highest peak rates (\~2,700 per 100k in 1991), while cities like Philadelphia and Los Angeles peaked lower but still showed substantial elevation
-   All cities show dramatic declines from peak to 2015, though the magnitude varies significantly
-   The temporal patterns are not uniform—some cities peaked earlier (Detroit in 1991) while others peaked later, revealing important geographic variation

**Visualization 2: Peak Crime Years Summary Table**

The summary table quantifies these trends, showing that peak years clustered between 1991-1993 for most cities, with declines ranging from 40-70% by 2015. This table enables analysts to quickly compare exact peak years and magnitudes across cities.

**How This Supports Decision-Making**:

For a policy analyst like Jordan (our persona), these visualizations answer critical questions:

-   **When** did crime peak in specific cities? (Enabling him to research what policies or events occurred around those years)
-   **How different** were peak magnitudes between cities? (Helping identify which cities faced the most severe challenges)
-   **What was the trajectory** before and after the peak? (Revealing whether interventions were followed by sustained declines or plateaus)

**Visualization 3: Total Crimes by Year and Category**

This stacked bar chart aggregates crime data across all 68 cities to show the overall temporal trends in violent crime from 1975 to 2015. Each bar represents a year, with different colors indicating the four violent crime categories: homicides, rapes, robberies, and aggravated assaults.

**Key Patterns Observed**:

-   **Rising trend (1975-early 1990s)**: Total violent crimes increased steadily, with a sharp acceleration in the late 1980s and early 1990s
-   **Peak period (\~1991-1993)**: The visualization shows the highest bars during this period, consistent with our individual city analysis
-   **Sustained decline (1993-2015)**: A dramatic decrease in total crimes, with 2015 levels approaching early 1980s numbers
-   **Crime composition**: Aggravated assaults and robberies constitute the majority of violent crimes across all years, while homicides represent a smaller but consistent proportion

**How This Supports User Story 2**:

This visualization directly addresses **User Story 2**: *"As a policy analyst, I want to compare violent and property crime trends so that I can understand whether different crime categories follow similar or divergent patterns over time."*

By displaying all four violent crime types in a single view, analysts can observe that: - All crime categories generally follow the same temporal pattern (rise and fall together) - However, the *magnitude* of change differs—robberies show a steeper decline than homicides - This suggests that while broad societal factors may affect all crime types, certain interventions may be more effective for specific categories

The year-over-year aggregation allows Jordan to identify national-level trends before drilling down into city-specific patterns, helping him distinguish between local anomalies and widespread phenomena.

By identifying that most major cities peaked around 1991-1993, Jordan can investigate whether common federal policies (e.g., community policing initiatives, crime bills) correlate with the subsequent decline, or whether local factors explain variation. The data's consistency and completeness across 41 years ensures these patterns are robust and actionable for policy analysis.

## Section 5: App Sketch & Description

<p align="center">
  <img src="../img/sketch.png" width="800">
</p>


The Crime Trends Dashboard follows a structured two-column layout designed to support interactive exploration of long-term UCR crime data from 1975–2015. The interface consists of a header, a left-side filter panel, summary statistic cards, and three primary visual components: a time-series chart, a geographic map, and a city comparison bar chart. The layout is designed to guide users from high-level summaries to detailed comparative analysis.

At the top of the dashboard, a header clearly identifies the scope of the analysis, indicating that the application focuses on historical crime trends across major U.S. cities. This provides contextual framing for the data being explored.

The left sidebar contains the primary interactive controls. Users can select one or multiple cities using a multi-select dropdown, adjust the year range using a slider spanning 1975 to 2015, and choose the crime category (e.g., violent crime or property crime) from a dropdown menu. A reset button allows users to quickly return to the default state of the dashboard. These filters update all visual components dynamically, enabling customized analysis of specific cities, time periods, and crime categories.

The top of the main content area contains summary statistic cards. These include the peak crime year within the selected time range and the current crime rate for the selected city or cities. These metrics provide immediate high-level insights before deeper analysis. The peak year indicator directly supports the identification of significant crime periods, while the displayed crime rate contextualizes the magnitude of the selected metric.

The primary visualization is a time-series line chart showing crime rates over time. The x-axis represents year, and the y-axis represents the selected crime rate (preferably per 100,000 population). When multiple cities are selected, each city is represented by a separate line, enabling direct comparison of long-term trends. This visualization supports analysis of sustained increases, declines, and timing differences across cities and crime categories.

A geographic map component displays selected cities across the United States. Color intensity represents the magnitude of crime rates, allowing users to quickly identify geographic patterns or regional clustering. The map updates based on selected filters and complements the time-series analysis by adding spatial context.

Finally, a bar chart provides side-by-side comparison of cities within a selected year or averaged over the chosen time range. This component allows users to compare magnitudes directly and identify which cities experienced larger increases or decreases during specific periods.

All components are interconnected. Adjusting filters dynamically updates summary statistics, the line chart, the map, and the comparison chart simultaneously. This coordinated interaction ensures that users can seamlessly move between temporal, geographic, and comparative perspectives while maintaining analytical consistency.


