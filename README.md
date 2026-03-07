# Crime Dashboard

## Description

This interactive crime dashboard visualizes annual crime data from 1975 to 2015 across major North American cities, enabling users to explore long-term trends and geographic patterns in public safety. Its central feature is an interactive, geocoded map that allows users to examine various crime rates by city. Together in combination with additional visualization, the tools populating this dashboard provide a data-driven, temporal view of how crime has evolved across North America.

## Deployed Dashboard

| Environment | Purpose | URL |
| :--- | :--- | :--- |
| **Main (Production)** | Stable version for public viewing | [View Live Dashboard](https://019c9723-a4d1-3cd7-eb5c-fa163f62eb99.share.connect.posit.cloud/) |
| **Development** | Testing new features and map logic | [View Dev Version](https://019c9728-2587-c2e2-7794-f6443291c277.share.connect.posit.cloud/) |

## Dashboard Preview

<img src="/img/demo.gif" alt="Dashboard Demo" width="1000">

## AI Explorer Tab

The dashboard includes an AI-powered tab that lets users query the crime dataset
using natural language, powered by [querychat](https://github.com/posit-dev/querychat)
and Anthropic's Claude.

**Features:**
- Natural language chat interface to filter and explore crime data
- Reactive data table showing filtered results
- Two interactive Altair visualizations (crime trend over time + city comparison bar chart)
- Download button to export the filtered dataset as CSV

**API Key Setup:**

The AI tab requires an Anthropic API key to function.

1. Create a `.env` file in the project root:
```
   ANTHROPIC_API_KEY=your-key-here
```
2. Make sure `.env` is listed in `.gitignore` (never commit your key).
3. For deployment on Posit Connect Cloud, set `ANTHROPIC_API_KEY` as an
   environment variable in the deployment settings.
   
   
## Instructions for Local Use

1. Clone the repository

```{bash}
git clone https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard.git
cd DSCI-532_2026_38_crime-dashboard
```

2. Create and activate environment

```{bash}
conda env create -f environment.yml
conda activate crime-dashboard
```

3. Run the app

```{bash}
python -m shiny run --reload src/app.py
```

### Notes:
If you would like to use this environment with Jupyter notebooks, register the kernel with:
```{bash}
python -m ipykernel install --user --name crime-dashboard --display-name "Python (crime-dashboard)"
jupyter lab
```

Contributor Instructions: <https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/blob/main/CONTRIBUTING.md>
