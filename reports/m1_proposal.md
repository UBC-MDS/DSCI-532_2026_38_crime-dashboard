## Section 1: Motivation and Purpose

> **Our role:** Data scientist consultancy firm
> **Target audience:** Public safety policy analysts and city-level decision makers (e.g., municipal public safety departments)
>
> Historical crime data contains decades of valuable information, but it is often stored in raw tabular formats that are difficult to interpret and compare. The city-level UCR dataset (1975–2015) published by The Marshall Project provides long-term crime statistics across major U.S. cities, yet extracting meaningful trends from a CSV file requires significant manual effort.
>
> Public safety analysts need to understand how violent and property crime have changed over time, identify peak periods, and compare patterns across cities. Without interactive tools, this process is slow, fragmented, and prone to oversimplification.
>
> To address this challenge, we propose building an interactive crime trends dashboard that allows policy analysts to visually explore long-term crime data. Our app will display trends over time, allow filtering by city and year range, and enable comparisons between crime categories and across multiple cities. By transforming raw data into clear visualizations, the dashboard will help decision makers identify patterns, detect anomalies, and generate evidence-based insights to inform public safety strategies.

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
