# Crime Dashboard

## Description

This interactive crime dashboard visualizes annual crime data from 1975 to 2015 across major North American cities, enabling users to explore long-term trends and geographic patterns in public safety. Its central feature is an interactive, geocoded map that allows users to examine various crime rates by city. Together in combination with additional visualization, the tools populating this dashboard provide a data-driven, temporal view of how crime has evolved across North America.

## Instructions for Use

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

### Note:
If you would like to use this environment with Jupyter notebooks, register the kernel with:
```{bash}
python -m ipykernel install --user --name crime-dashboard --display-name "Python (crime-dashboard)"
jupyter lab
```
