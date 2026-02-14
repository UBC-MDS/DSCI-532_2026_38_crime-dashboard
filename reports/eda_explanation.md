## Section 4: Exploratory Data Analysis

### Dataset Structure

**Key Variables**:

-   **Geographic/Temporal**: `department_name` (city), `year` (1975-2015), `ORI` (agency identifier)
-   **Population**: `total_pop` (city population for rate calculations)
-   **Violent Crime Totals**: `violent_crime` (sum of all violent offenses), `homs_sum` (homicides), `rape_sum`, `rob_sum` (robberies), `agg_ass_sum` (aggravated assaults)
-   **Crime Rates**: `violent_per_100k`, `homs_per_100k`, `rape_per_100k`, `rob_per_100k`, `agg_ass_per_100k` (all normalized per 100,000 population)
-   **Data Quality**: `months_reported` (indicates completeness of annual reporting)
-   **Rows in Dataset**: 2898

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
