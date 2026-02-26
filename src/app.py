from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "ucr_crime_1975_2015.csv"
crimes_df = pd.read_csv(DATA_PATH)

app_ui = ui.page_fillable(

    ui.h2("Crime Trends Dashboard (1975–2015)"),

    ui.layout_sidebar(

        ui.sidebar(
            ui.input_selectize(
                "city",
                "Select City",
                choices=sorted(crimes_df["department_name"].unique()),
                multiple=True,
            ),
            ui.input_slider(
                "year_range",
                "Year Range",
                min=int(crimes_df["year"].min()),
                max=int(crimes_df["year"].max()),
                value=(
                    int(crimes_df["year"].min()),
                    int(crimes_df["year"].max()),
                ),
                step=1,
            ),
            ui.input_select(
                "crime_type",
                "Crime Type",
                choices=[
                    "Violent Crime",
                    "Homicide",
                    "Rape",
                    "Robbery",
                    "Aggravated Assault",
                ],
            ),
            ui.input_action_button("reset", "Reset Filters"),
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Peak Crime Year"),
                ui.output_ui("peak_year"),
            ),
            ui.card(
                ui.card_header("Crime Rate"),
                ui.output_ui("crime_rate"),
            ),
            col_widths=(6, 6),
        ),

        ui.card(
            ui.card_header("Trend Over Time"),
            ui.output_plot("trend_plot"),
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Map View"),
                "Placeholder: Map visualization.",
            ),
            ui.card(
                ui.card_header("City Comparison"),
                "Placeholder: Bar chart comparison.",
            ),
            col_widths=(6, 6),
        ),
    ),
)

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
            value=(
                int(crimes_df["year"].min()),
                int(crimes_df["year"].max()),
            ),
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
            return "No data"
        idx = df[col].idxmax()
        return ui.h3(str(int(df.loc[idx, "year"])))

    @output
    @render.ui
    def crime_rate():
        df = filtered_df()
        col = selected_column()
        if df.empty:
            return "No data"
        return ui.h3(f"{df[col].mean():.1f} per 100k")

    @output
    @render.plot
    def trend_plot():
        df = filtered_df()
        col = selected_column()

        fig, ax = plt.subplots(figsize=(8, 5))

        if df.empty:
            ax.text(0.5, 0.5, "No data for selected filters",
                    ha="center", va="center")
            ax.set_axis_off()
            return fig

        for city, group in df.groupby("department_name"):
            ax.plot(group["year"], group[col], label=city)

        ax.set_xlabel("Year")
        ax.set_ylabel("Rate per 100k")
        ax.set_title(f"{input.crime_type()} Trend")
        ax.legend()
        return fig

app = App(app_ui, server)