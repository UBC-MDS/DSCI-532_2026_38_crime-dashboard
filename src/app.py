from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt
from vega_datasets import data as vega_data
from shiny import req
from faicons import icon_svg



plt.rcParams.update(
    {
        "figure.dpi": 120,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
    }
)


# Data

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "ucr_crime_1975_2015.csv"
crimes_df = pd.read_csv(DATA_PATH)


# UI

app_ui = ui.page_fillable(
    
    ui.tags.head(
                ui.tags.link(
                    rel="stylesheet",
                    href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/flatly/bootstrap.min.css",
                ),
                ui.include_css("www/styles.css"),
            ),
    
    ui.navset_tab(

        ui.nav_panel(
            "Crime Dashboard",
            ui.div(
        {"class": "app-header"},
        ui.h2("CRIME TRENDS"),
        ui.div(
            {"class": "header-sub"},
            ui.span("(1975–2015)", class_="chip"),
            ui.span(" Rates per 100k residents • U.S. departments", class_="muted"),
        ),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            {"class": "sidebar-card"},
            ui.h6("Filters", class_="sidebar-title"),
            ui.input_selectize(
                "city",
                "Select City (max 6)",
                choices=sorted(crimes_df["department_name"].unique()),
                multiple=True,
                options={"placeholder": "Type to search cities...", "maxItems": 6},
            ),
            ui.input_slider(
                "year_range",
                "Year Range",
                min=int(crimes_df["year"].min()),
                max=int(crimes_df["year"].max()),
                value=(int(crimes_df["year"].min()), int(crimes_df["year"].max())),
                step=1,
            ),
            ui.hr(),
            ui.h6("Map Controls", class_="sidebar-title"),
            ui.input_slider(
                "map_year",
                "Map Year",
                min=int(crimes_df["year"].min()),
                max=int(crimes_df["year"].max()),
                value=int(crimes_df["year"].max()),
                step=5,
                sep=""
            ),
            ui.input_select(
                "map_color_scheme",
                "Color Scheme",
                choices={
                    "None": "Select Color",
                    "orangered": "Orange-Red",
                    "reds": "Reds",
                    "blues": "Blues",
                    "purples": "Purples"
                },
                selected="None"
            ),
            ui.input_select(
                "crime_type",
                "Crime Metric",
                choices=["None","Violent Crime", "Homicide", "Rape", "Robbery", "Aggravated Assault"],
                selected="None"
            ),
            ui.input_action_button(
                "reset",
                "RESET",
                icon=icon_svg("rotate-left"), # Adds a reset arrow icon
                class_="btn btn-dark w-100 reset-btn",
            ),
        ),
        ui.layout_columns(
            ui.card(
                {"class": "kpi-card"},
                ui.card_header("Peak Crime Year"),
                ui.output_ui("peak_year"),
            ),
            ui.card(
                {"class": "kpi-card"},
                ui.card_header("Average Rate"),
                ui.output_ui("crime_rate"),
                ui.div("per 100k residents", class_="kpi-sub"),
            ),
            col_widths=(7, 5),
        ),
        ui.card(
            {"class": "plot-card"},
            ui.card_header(
                ui.div(
                    {"class": "card-header-row"},
                    ui.span("Trend Over Time"),
                    ui.span(" (Tip: Select ≤6 cities for a clean plot)", class_="muted small"),
                )
            ),
            ui.output_plot("trend_plot"),
        ),
        ui.layout_columns(
            ui.card(
                {"class": "plot-card"},
                ui.card_header("Geographic Distribution by State"),
                ui.div("States colored by average crime rate across cities", class_="muted small pad-b"),
                ui.output_ui("choropleth_map"),
            ),
            ui.card(
                {"class": "plot-card"},
                ui.card_header("City Comparison"),
                ui.div("Average over selected years", class_="muted small pad-b"),
                ui.output_plot("city_comparison_plot"),
            ),
            col_widths=(7, 5),
        ),
    ),
        ),
        ui.nav_panel(
            "Analysis Page",
            ui.h3("Chatbot"),
            ui.p("You can add new charts, tables, or maps here.")
        )
    )
)


# Server

def server(input, output, session):

    def selected_column():

        if input.crime_type() == "None":
            return None
    
        mapping = {
            "Violent Crime": "violent_per_100k",
            "Homicide": "homs_per_100k",
            "Rape": "rape_per_100k",
            "Robbery": "rob_per_100k",
            "Aggravated Assault": "agg_ass_per_100k",
        }
        return mapping[input.crime_type()]

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_selectize("city", selected=[])
        ui.update_slider(
            "year_range",
            value=(int(crimes_df["year"].min()), int(crimes_df["year"].max())),
        )
        ui.update_select("crime_type", selected="None") # This triggers the map to hide
        ui.update_slider("map_year", value=int(crimes_df["year"].max()))
        ui.update_select("map_color_scheme", selected="None")


    @reactive.calc
    def filtered_df():
        df = crimes_df.copy()
        start, end = input.year_range()
        df = df[(df["year"] >= start) & (df["year"] <= end)]
        if input.city():
            df = df[df["department_name"].isin(input.city())]
        return df
    
    
    # Helper function for state aggregation - COMPLETE MAPPING
    def prepare_state_data(df, year, metric):
        """Aggregate city crime data to state level for choropleth."""
        
        df_year = df[df["year"] == year].copy()
        
        if df_year.empty:
            return pd.DataFrame(columns=['id', 'state_name', 'crime_rate', 'num_cities'])
        
        # COMPLETE city-to-state mapping (covers all 69 cities)
        city_to_state = {
            # Cities WITH state abbreviation in name
            'Albuquerque, N.M.': 'New Mexico',
            'Arlington, Texas': 'Texas',
            'Aurora, Colo.': 'Colorado',
            'Austin, Texas': 'Texas',
            'Baltimore County, Md.': 'Maryland',
            'Buffalo, N.Y.': 'New York',
            'Charlotte-Mecklenburg, N.C.': 'North Carolina',
            'Columbus, Ohio': 'Ohio',
            'El Paso, Texas': 'Texas',
            'Fairfax County, Va.': 'Virginia',
            'Fort Worth, Texas': 'Texas',
            'Fresno, Calif.': 'California',
            'Jacksonville, Fla.': 'Florida',
            'Kansas City, Mo.': 'Missouri',
            'Long Beach, Calif.': 'California',
            'Los Angeles County, Calif.': 'California',
            'Louisville, Ky.': 'Kentucky',
            'Memphis, Tenn.': 'Tennessee',
            'Mesa, Ariz.': 'Arizona',
            'Miami-Dade County, Fla.': 'Florida',
            'Montgomery County, Md.': 'Maryland',
            'Nashville, Tenn.': 'Tennessee',
            'Nassau County, N.Y.': 'New York',
            'Newark, N.J.': 'New Jersey',
            'Oakland, Calif.': 'California',
            'Omaha, Neb.': 'Nebraska',
            'Orlando, Fla.': 'Florida',
            'Portland, Ore.': 'Oregon',
            'Prince Georges County, Md.': 'Maryland',
            "Prince George's County, Md.": 'Maryland',
            'Raleigh, N.C.': 'North Carolina',
            'Sacramento, Calif.': 'California',
            'San Diego, Calif.': 'California',
            'San Jose, Calif.': 'California',
            'St. Louis, Mo.': 'Missouri',
            'St. Paul, Minn.': 'Minnesota',
            'Suffolk County, N.Y.': 'New York',
            'Tampa, Fla.': 'Florida',
            'Tucson, Ariz.': 'Arizona',
            'Tulsa, Okla.': 'Oklahoma',
            'Virginia Beach, Va.': 'Virginia',
            'Washington, D.C.': 'District of Columbia',
            'Wichita, Kan.': 'Kansas',
            
            # Cities WITHOUT state abbreviation in name (30 major cities)
            'Atlanta': 'Georgia',
            'Baltimore': 'Maryland',
            'Boston': 'Massachusetts',
            'Chicago': 'Illinois',
            'Cincinnati': 'Ohio',
            'Cleveland': 'Ohio',
            'Dallas': 'Texas',
            'Denver': 'Colorado',
            'Detroit': 'Michigan',
            'Honolulu': 'Hawaii',
            'Houston': 'Texas',
            'Indianapolis': 'Indiana',
            'Las Vegas': 'Nevada',
            'Los Angeles': 'California',
            'Miami': 'Florida',
            'Milwaukee': 'Wisconsin',
            'Minneapolis': 'Minnesota',
            'New Orleans': 'Louisiana',
            'New York City': 'New York',
            'Oklahoma City': 'Oklahoma',
            'Philadelphia': 'Pennsylvania',
            'Phoenix': 'Arizona',
            'Pittsburgh': 'Pennsylvania',
            'Salt Lake City': 'Utah',
            'San Antonio': 'Texas',
            'San Diego': 'California',
            'San Francisco': 'California',
            'San Jose': 'California',
            'Seattle': 'Washington',
            
            # Special cases
            'National': None  
        }
        
        # Map department names to states
        df_year['state_name'] = df_year['department_name'].map(city_to_state)
        
        # Drop rows without state mapping (like "National")
        df_year = df_year.dropna(subset=['state_name'])
        
        # Aggregate to state level
        state_agg = df_year.groupby('state_name').agg({
            metric: 'mean',
            'department_name': 'count'
        }).reset_index()
        
        state_agg.columns = ['state_name', 'crime_rate', 'num_cities']
        
        # Map to FIPS codes for Vega data
        fips = {
            'Alabama': 1, 'Arizona': 4, 'California': 6, 'Colorado': 8,
            'Connecticut': 9, 'District of Columbia': 11, 'Florida': 12,
            'Georgia': 13, 'Hawaii': 15, 'Illinois': 17, 'Indiana': 18,
            'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22, 'Maryland': 24, 
            'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27, 'Missouri': 29, 
            'Nebraska': 31, 'Nevada': 32, 'New Jersey': 34, 'New Mexico': 35, 
            'New York': 36, 'North Carolina': 37, 'Ohio': 39, 'Oklahoma': 40, 
            'Oregon': 41, 'Pennsylvania': 42, 'Tennessee': 47, 'Texas': 48, 
            'Utah': 49, 'Virginia': 51, 'Washington': 53, 'Wisconsin': 55
        }
        
        state_agg['id'] = state_agg['state_name'].map(fips)
        state_agg = state_agg.dropna(subset=['id'])
        state_agg['id'] = state_agg['id'].astype(int)
        
        return state_agg

    @output
    @render.ui
    def peak_year():

        col = selected_column()
        df = filtered_df()
        
        if df.empty:
            return ui.h3("N Colums", class_="kpi-val")
        
        try:
            idx = df[col].idxmax()
            val = str(int(df.loc[idx, "year"]))
            return ui.h3(val, class_="kpi-val")
        except (KeyError, ValueError):
            return ui.h3("Select a City", class_="kpi-val")

    @output
    @render.ui
    def crime_rate():
        
        col = selected_column()
        df = filtered_df()
        
        # Check 
        if col is None or df.empty:
            return ui.h3("Select a City", class_="kpi-val")

        # 3. Calculate mean safely
        try:
            avg_val = df[col].mean()
            return ui.h3(f"{avg_val:.1f}", class_="kpi-val")
        except (KeyError, TypeError):
            return ui.h3("-", class_="kpi-val")
    

    @output
    @render.plot
    def trend_plot():
        df = filtered_df()
        col = selected_column()
        req(col is not None)
        fig, ax = plt.subplots(figsize=(10, 4.8))

        # IMPORTANT: don't spaghetti-plot all cities by default
        if not input.city():
            ax.text(0.5, 0.5, "Select 1+ cities to view trends", ha="center", va="center")
            ax.set_axis_off()
            return fig

        if df.empty:
            ax.text(0.5, 0.5, "No data for selected filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        for city, group in df.groupby("department_name"):
            ax.plot(group["year"], group[col], label=city)

        ax.set_xlabel("Year")
        ax.set_ylabel("Rate per 100k")
        ax.set_title(f"{input.crime_type()} Trend")

        # only show legend if not too many cities
        if len(input.city()) <= 6:
            ax.legend()

        fig.tight_layout()
        return fig

    @output
    @render.plot
    def city_comparison_plot():
        df = filtered_df()
        col = selected_column()
        req(col is not None)
        fig, ax = plt.subplots(figsize=(10, 4.8))

        if not input.city():
            ax.text(0.5, 0.5, "Select 1+ cities to compare", ha="center", va="center")
            ax.set_axis_off()
            return fig

        if df.empty:
            ax.text(0.5, 0.5, "No data for selected filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        summary = (
            df.groupby("department_name", as_index=False)[col]
            .mean()
            .sort_values(col, ascending=False)
        )

        ax.bar(summary["department_name"], summary[col])
        ax.set_ylabel("Average rate per 100k")
        start, end = input.year_range()
        ax.set_title(f"{input.crime_type()} Average ({start}–{end})")
        ax.tick_params(axis="x", rotation=35)

        fig.tight_layout()
        return fig
    

    @output
    @render.ui
    def choropleth_map():
        """Render choropleth map showing crime rates by state."""

        color_scheme = input.map_color_scheme()
        year = input.map_year()
        col = selected_column()

        if color_scheme == "None" or col is None:
            return ui.div(
                ui.h4("Map Configuration Incomplete"),
                ui.p("Please select both a Crime Metric and a Color Scheme to view the map."),
                style="text-align: center; padding: 100px; color: #999; border: 1px dashed #ccc; border-radius: 8px;"
            )
    
        if input.crime_type() == "None":
            return ui.div(style="height: 400px; display: flex; align-items: center; justify-content: center; color: #aaa;", 
                      children="Map hidden. Select a metric to visualize."), ui.h3("Select a City", class_="kpi-val")

        
        # Use full dataset for map (not filtered by cities)
        state_data = prepare_state_data(crimes_df, year, col)
        
        if state_data.empty:
            return ui.div(
                "No data available for selected year",
                class_="placeholder-box",
                style="text-align: center; padding: 50px;"
            )
        
        # Load US states geography
        states = alt.topo_feature(vega_data.us_10m.url, 'states')
        
        # Background layer (all states in gray)
        background = alt.Chart(states).mark_geoshape(
            fill='lightgray',
            stroke='white',
            strokeWidth=1
        ).project('albersUsa').properties(
            width='container',
            height=400
        )
        
        # Choropleth layer (states with data)
        choropleth = alt.Chart(states).mark_geoshape(
            stroke='white',
            strokeWidth=1
        ).encode(
            color=alt.Color(
                'crime_rate:Q',
                scale=alt.Scale(
                    scheme=input.map_color_scheme(),
                    domain=[0, state_data['crime_rate'].max()]
                ),
                legend=alt.Legend(
                    title='Rate per 100k',
                    orient='bottom',
                    direction='horizontal',
                    gradientLength=300
                )
            ),
            tooltip=[
                alt.Tooltip('state_name:N', title='State'),
                alt.Tooltip('crime_rate:Q', title='Crime Rate', format='.1f'),
                alt.Tooltip('num_cities:Q', title='Cities in Dataset')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(
                state_data,
                'id',
                ['crime_rate', 'state_name', 'num_cities']
            )
        ).project('albersUsa').properties(
            width='container',
            height=400,
            title={
                "text": f"{input.crime_type()} Rate by State — {year}",
                "fontSize": 14
            }
        )
        
        # Combine layers
        final_map = background + choropleth
        
        return ui.HTML(final_map.to_html())


app = App(app_ui, server)