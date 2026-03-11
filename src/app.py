from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt
from vega_datasets import data as vega_data
from shiny import req
from faicons import icon_svg
from querychat import QueryChat
from dotenv import load_dotenv
import duckdb

load_dotenv()

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


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

BASE_DIR    = Path(__file__).resolve().parent.parent
PARQUET_PATH = BASE_DIR / "data" / "processed" / "crime.parquet"

# Single persistent read-only connection shared across all reactive contexts.
# DuckDB can query parquet directly without loading the full file into memory.
con = duckdb.connect(database=":memory:", read_only=False)
con.execute(f"CREATE VIEW crimes AS SELECT * FROM read_parquet('{PARQUET_PATH}')")

# ---------------------------------------------------------------------------
# Startup metadata queries — cheap, column-statistics only, no full scan
# ---------------------------------------------------------------------------

_meta = con.execute(
    "SELECT MIN(year) AS yr_min, MAX(year) AS yr_max FROM crimes"
).fetchone()
YEAR_MIN: int = int(_meta[0])
YEAR_MAX: int = int(_meta[1])

CITY_CHOICES: list[str] = sorted(
    row[0]
    for row in con.execute(
        "SELECT DISTINCT department_name FROM crimes ORDER BY department_name"
    ).fetchall()
)

# ---------------------------------------------------------------------------
# QueryChat — needs a real DataFrame at init time.
# We load from parquet (fast, columnar), but this is a one-time cost
# isolated to the AI tab; it does NOT affect the main dashboard's lazy path.
# ---------------------------------------------------------------------------

_qc_df = pd.read_parquet(PARQUET_PATH)

qc = QueryChat(
    _qc_df,
    "crime_data",
    data_description=(BASE_DIR / "data" / "data_description.md"),
    client="anthropic/claude-sonnet-4-20250514",
)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

app_ui = ui.page_fillable(

    ui.tags.head(
         # Bootswatch "Flatly" theme (professional look)
        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/flatly/bootstrap.min.css",
        ),
        ui.include_css("www/styles.css"),
        ui.tags.script(src="https://cdn.jsdelivr.net/npm/vega@5"),
        ui.tags.script(src="https://cdn.jsdelivr.net/npm/vega-lite@5"),
        ui.tags.script(src="https://cdn.jsdelivr.net/npm/vega-embed@6"),
    ),

    ui.navset_tab(
        # ------------------------------------------------------------------
        # Tab 1: Crime Dashboard
        # ------------------------------------------------------------------
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
                        choices=CITY_CHOICES,          # from metadata query
                        multiple=True,
                        options={"placeholder": "Type to search cities...", "maxItems": 6},
                    ),
                    ui.input_slider(
                        "year_range",
                        "Year Range",
                        min=YEAR_MIN,
                        max=YEAR_MAX,
                        value=(YEAR_MIN, YEAR_MAX),
                        step=1,
                    ),
                    ui.hr(),
                    ui.h6("Map Controls", class_="sidebar-title"),
                    ui.input_slider(
                        "map_year",
                        "Map Year",
                        min=YEAR_MIN,
                        max=YEAR_MAX,
                        value=YEAR_MAX,
                        step=5,
                        sep=""
                    ),
                    ui.input_select(
                        "crime_type",
                        "Crime Metric",
                        choices=["None", "Violent Crime", "Homicide", "Rape", "Robbery", "Aggravated Assault"],
                        selected="None"
                    ),
                    ui.input_action_button(
                        "reset",
                        "RESET",
                        icon=icon_svg("rotate-left"),
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

        # ------------------------------------------------------------------
        # Tab 2: AI Explorer
        # ------------------------------------------------------------------
        ui.nav_panel(
            "AI Explorer",
            ui.page_sidebar(
                ui.sidebar(qc.ui()),
                ui.layout_columns(
                    ui.card(
                        {"class": "kpi-card"},
                        ui.card_header("Rows in Filtered Data"),
                        ui.output_ui("ai_row_count"),
                    ),
                    ui.card(
                        {"class": "kpi-card"},
                        ui.card_header("Cities in Filtered Data"),
                        ui.output_ui("ai_city_count"),
                    ),
                    col_widths=(6, 6),
                ),
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Violent Crime Trend Over Time"),
                        ui.output_ui("ai_trend_chart"),
                    ),
                    ui.card(
                        ui.card_header("Crime Rate by City"),
                        ui.output_ui("ai_city_bar_chart"),
                    ),
                    col_widths=(6, 6),
                ),
                ui.card(
                    ui.card_header("Filtered Crime Data"),
                    ui.output_data_frame("ai_data_table"),
                    ui.download_button("ai_download", "Download Filtered Data", class_="btn btn-dark mt-2"),
                ),
            ),
        ),
    ),
)


# ---------------------------------------------------------------------------
# Helper: city -> state mapping and FIPS (unchanged logic, moved to module level)
# ---------------------------------------------------------------------------

CITY_TO_STATE: dict[str, str | None] = {
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
    'National': None,
}

STATE_FIPS: dict[str, int] = {
    'Alabama': 1, 'Arizona': 4, 'California': 6, 'Colorado': 8,
    'Connecticut': 9, 'District of Columbia': 11, 'Florida': 12,
    'Georgia': 13, 'Hawaii': 15, 'Illinois': 17, 'Indiana': 18,
    'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22, 'Maryland': 24,
    'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27, 'Missouri': 29,
    'Nebraska': 31, 'Nevada': 32, 'New Jersey': 34, 'New Mexico': 35,
    'New York': 36, 'North Carolina': 37, 'Ohio': 39, 'Oklahoma': 40,
    'Oregon': 41, 'Pennsylvania': 42, 'Tennessee': 47, 'Texas': 48,
    'Utah': 49, 'Virginia': 51, 'Washington': 53, 'Wisconsin': 55,
}

CRIME_METRIC_MAP: dict[str, str] = {
    "Violent Crime": "violent_per_100k",
    "Homicide":      "homs_per_100k",
    "Rape":          "rape_per_100k",
    "Robbery":       "rob_per_100k",
    "Aggravated Assault": "agg_ass_per_100k",
}


def prepare_state_data_from_db(
    conn: duckdb.DuckDBPyConnection,
    year: int,
    metric: str,
) -> pd.DataFrame:
    """
    Aggregate city crime data to state level.
    All filtering happens inside DuckDB — only the aggregated rows (one per
    state, ~35 rows max) are pulled into a DataFrame.
    """
    # Pull only the two columns we need for the requested year
    rows = conn.execute(
        f"""
        SELECT department_name, "{metric}"
        FROM crimes
        WHERE year = ?
          AND "{metric}" IS NOT NULL
        """,
        [year],
    ).fetchall()

    if not rows:
        return pd.DataFrame(columns=["id", "state_name", "crime_rate", "num_cities"])

    # Map city -> state in Python (lookup table, O(n) on ~60 rows)
    records = []
    for dept, rate in rows:
        state = CITY_TO_STATE.get(dept)
        if state is not None:
            records.append({"state_name": state, "crime_rate": rate})

    if not records:
        return pd.DataFrame(columns=["id", "state_name", "crime_rate", "num_cities"])

    agg = (
        pd.DataFrame(records)
        .groupby("state_name")
        .agg(crime_rate=("crime_rate", "mean"), num_cities=("crime_rate", "count"))
        .reset_index()
    )
    agg["id"] = agg["state_name"].map(STATE_FIPS)
    agg = agg.dropna(subset=["id"])
    agg["id"] = agg["id"].astype(int)
    return agg


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

def server(input, output, session):
    
    @reactive.calc
    def selected_column() -> str | None:
        crime = input.crime_type()
        if crime == "None":
            return None
        return CRIME_METRIC_MAP.get(crime)

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_selectize("city", selected=[])
        ui.update_slider("year_range", value=(YEAR_MIN, YEAR_MAX))
        ui.update_select("crime_type", selected="None")
        ui.update_slider("map_year", value=YEAR_MAX)

    # ------------------------------------------------------------------
    # Core lazy query — ALL filtering happens here inside DuckDB.
    # Nothing downstream receives more rows than this query returns.
    # ------------------------------------------------------------------

    @reactive.calc
    def filtered_df() -> pd.DataFrame:
        start, end = input.year_range()
        cities = list(input.city())

        if cities:
            # Parameterised IN clause — DuckDB handles the list natively
            placeholders = ", ".join("?" * len(cities))
            query = f"""
                SELECT *
                FROM crimes
                WHERE year BETWEEN ? AND ?
                  AND department_name IN ({placeholders})
            """
            params = [start, end] + cities
        else:
            query = """
                SELECT *
                FROM crimes
                WHERE year BETWEEN ? AND ?
            """
            params = [start, end]

        return con.execute(query, params).df()

    # ------------------------------------------------------------------
    # KPI outputs
    # ------------------------------------------------------------------

    @output
    @render.ui
    def peak_year():
        col = selected_column()
        df  = filtered_df()
        if col is None or df.empty:
            return ui.h6("Select a type of Crime", class_="kpi-val")
        try:
            idx = df[col].idxmax()
            return ui.h3(str(int(df.loc[idx, "year"])), class_="kpi-val")
        except (KeyError, ValueError):
            return ui.h6("Select a type of Crime", class_="kpi-val")

    @output
    @render.ui
    def crime_rate():
        col = selected_column()
        df  = filtered_df()
        if col is None or df.empty:
            return ui.h6("Select a type of Crime", class_="kpi-val")
        try:
            return ui.h3(f"{df[col].mean():.1f}", class_="kpi-val")
        except (KeyError, TypeError):
            return ui.h3("-", class_="kpi-val")

    # ------------------------------------------------------------------
    # Trend plot
    # ------------------------------------------------------------------

    @output
    @render.plot
    def trend_plot():
        df  = filtered_df()
        col = selected_column()
        req(col is not None)

        fig, ax = plt.subplots(figsize=(10, 4.8))

        if not input.city():
            ax.text(0.5, 0.5, "Select 1+ cities to view trends", ha="center", va="center")
            ax.set_axis_off()
            return fig

        if df.empty:
            ax.text(0.5, 0.5, "No data for selected filters", ha="center", va="center")
            ax.set_axis_off()
            return fig

        colors = plt.cm.tab10.colors
        selected_cities = sorted(input.city())
        city_colors = {city: colors[i % len(colors)] for i, city in enumerate(selected_cities)}

        for city, group in df.groupby("department_name"):
            ax.plot(group["year"], group[col], label=city, color=city_colors[city])

        ax.set_xlabel("Year")
        ax.set_ylabel("Rate per 100k")
        ax.set_title(f"{input.crime_type()} Trend Over Time")

        if len(input.city()) <= 6:
            ax.legend()

        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # City comparison bar chart
    # ------------------------------------------------------------------

    @output
    @render.plot
    def city_comparison_plot():
        df  = filtered_df()
        col = selected_column()
        req(col is not None)

        fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

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
            .sort_values(col, ascending=True)
        )

        colors = plt.cm.tab10.colors
        selected_cities = sorted(input.city())
        city_colors = {city: colors[i % len(colors)] for i, city in enumerate(selected_cities)}
        bar_colors = [city_colors[city] for city in summary["department_name"]]

        ax.barh(summary["department_name"], summary[col], color=bar_colors)
        ax.set_xlabel("Average rate per 100k", fontsize=9)
        ax.set_title("City Comparison", fontsize=10)
        ax.tick_params(axis="y", labelsize=8)
        ax.tick_params(axis="x", labelsize=8)

        return fig

    # ------------------------------------------------------------------
    # Choropleth map
    # ------------------------------------------------------------------

    @output
    @render.ui
    def choropleth_map():
        crime_type = input.crime_type()
        year       = input.map_year()

        if crime_type == "None":
            return ui.div(
                ui.h4("Map Reset"),
                ui.p("Select a Crime Metric to visualize the map."),
                style="text-align:center;padding:100px;color:#999;border:1px dashed #ccc;border-radius:10px;"
            )

        col = CRIME_METRIC_MAP.get(crime_type)

        # Filtering happens inside DuckDB; only ~35 aggregated state rows enter Python
        state_data = prepare_state_data_from_db(con, year, col)

        if state_data.empty:
            return ui.div(
                "No data available for selected year",
                style="text-align:center;padding:50px;color:#999;"
            )

        states = alt.topo_feature(vega_data.us_10m.url, "states")

        background = alt.Chart(states).mark_geoshape(
            fill="lightgray", stroke="white", strokeWidth=1
        ).project("albersUsa")

        choropleth = alt.Chart(states).mark_geoshape(
            stroke="white", strokeWidth=1
        ).encode(
            color=alt.Color(
                "crime_rate:Q",
                scale=alt.Scale(scheme="reds", domain=[0, state_data["crime_rate"].max()]),
                legend=alt.Legend(
                    title="Rate per 100k", orient="bottom",
                    direction="horizontal", gradientLength=300
                ),
            ),
            tooltip=[
                alt.Tooltip("state_name:N", title="State"),
                alt.Tooltip("crime_rate:Q", title="Crime Rate", format=".1f"),
                alt.Tooltip("num_cities:Q", title="Cities in Dataset"),
            ],
        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(state_data, "id", ["crime_rate", "state_name", "num_cities"]),
        ).project("albersUsa")

        final_map = alt.layer(background, choropleth).properties(
            width="container",
            height=400,
            title=f"{crime_type} Rate by State — {year}"
        ).configure_view(
            strokeWidth=0
        )
    
        return ui.div(
                        {"id": "map-container", "class": "altair-map"},
                        ui.HTML(final_map.to_html())
                        )

    # ------------------------------------------------------------------
    # AI Explorer tab (QueryChat drives its own reactive filtered df)
    # ------------------------------------------------------------------

    qc_vals = qc.server()

    # KPI: Row count
    @output
    @render.ui
    def ai_row_count():
        return ui.h3(f"{len(qc_vals.df()):,}", class_="kpi-val")

    # KPI: Unique city count
    @output
    @render.ui
    def ai_city_count():
        df = qc_vals.df()
        n  = df["department_name"].nunique() if "department_name" in df.columns else 0
        return ui.h3(str(n), class_="kpi-val")

    # Plot 1: Violent crime trend over time (line chart)
    @output
    @render.ui
    def ai_trend_chart():
        df = qc_vals.df()
        if df.empty or "year" not in df.columns or "violent_per_100k" not in df.columns:
            return ui.p("No data to display. Try asking a question in the chat!",
                        style="text-align:center;padding:40px;color:#999;")

        if "department_name" in df.columns and df["department_name"].nunique() <= 10:
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X("year:O", title="Year"),
                y=alt.Y("violent_per_100k:Q", title="Violent Crime per 100k"),
                color=alt.Color("department_name:N", title="City"),
                tooltip=["department_name:N", "year:O", "violent_per_100k:Q"],
            ).properties(width="container", height=350)
        else:
            yearly = df.groupby("year", as_index=False)["violent_per_100k"].mean()
            chart = alt.Chart(yearly).mark_line(point=True).encode(
                x=alt.X("year:O", title="Year"),
                y=alt.Y("violent_per_100k:Q", title="Avg Violent Crime per 100k"),
                tooltip=["year:O", "violent_per_100k:Q"],
            ).properties(width="container", height=350)

        return ui.div(
                    {"id": "ai-trend-container", "class": "altair-chart"},
                    ui.HTML(chart.to_html())
                    )

    # Plot 2: Crime rate by city (bar chart)
    @output
    @render.ui
    def ai_city_bar_chart():
        df = qc_vals.df()
        if df.empty or "department_name" not in df.columns or "violent_per_100k" not in df.columns:
            return ui.p("No data to display. Try asking a question in the chat!",
                        style="text-align:center;padding:40px;color:#999;")

        city_avg = (
            df.groupby("department_name", as_index=False)["violent_per_100k"]
            .mean()
            .sort_values("violent_per_100k", ascending=False)
            .head(20)
        )

        chart = alt.Chart(city_avg).mark_bar().encode(
            x=alt.X("department_name:N", sort="-y", title="City",
                     axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("violent_per_100k:Q", title="Avg Violent Crime per 100k"),
            tooltip=["department_name:N", "violent_per_100k:Q"],
            color=alt.value("#2c3e50"),
        ).properties(width="container", height=350)

        return ui.div(
                        {"id": "ai-bar-container", "class": "altair-chart"},
                        ui.HTML(chart.to_html())
                    )

    @render.data_frame
    def ai_data_table():
        return qc_vals.df()

    @render.download(filename="filtered_crime_data.csv")
    def ai_download():
        yield qc_vals.df().to_csv(index=False)


app = App(app_ui, server)
