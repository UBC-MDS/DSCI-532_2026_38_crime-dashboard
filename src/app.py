from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



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
        # Bootswatch "Flatly" theme (professional look)
        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/flatly/bootstrap.min.css",
        ),
        # Your custom CSS (make sure file exists at: crime-dashboard/www/styles.css)
        ui.include_css("www/styles.css"),
    ),
    ui.div(
        {"class": "app-header"},
        ui.h2("CRIME TRENDS"),
        ui.div(
            {"class": "header-sub"},
            ui.span("1975–2015", class_="chip"),
            ui.span("Rates per 100k residents • U.S. departments", class_="muted"),
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
            ui.input_select(
                "crime_type",
                "Crime Metric",
                choices=["Violent Crime", "Homicide", "Rape", "Robbery", "Aggravated Assault"],
            ),
            ui.input_action_button(
                "reset",
                "RESET",
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
                    ui.span("Tip: select ≤6 cities for a clean plot", class_="muted small"),
                )
            ),
            ui.output_plot("trend_plot"),
        ),
        ui.layout_columns(
            ui.card(
                {"class": "plot-card"},
                ui.card_header("Map View"),
                ui.div("Map coming soon.", class_="placeholder-box"),
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
)


# Server

def server(input, output, session):
    def selected_column():
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
        ui.update_select("crime_type", selected="Violent Crime")

    @reactive.calc
    def filtered_df():
        df = crimes_df.copy()
        start, end = input.year_range()
        df = df[(df["year"] >= start) & (df["year"] <= end)]
        if input.city():
            df = df[df["department_name"].isin(input.city())]
        return df

    @output
    @render.ui
    def peak_year():
        df = filtered_df()
        col = selected_column()
        if df.empty:
            return ui.h3("—", class_="kpi-val")
        idx = df[col].idxmax()
        return ui.h3(str(int(df.loc[idx, "year"])), class_="kpi-val")

    @output
    @render.ui
    def crime_rate():
        df = filtered_df()
        col = selected_column()
        if df.empty:
            return ui.h3("—", class_="kpi-val")
        return ui.h3(f"{df[col].mean():.1f}", class_="kpi-val")

    @output
    @render.plot
    def trend_plot():
        df = filtered_df()
        col = selected_column()
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


app = App(app_ui, server)