from shiny import App, ui

app_ui = ui.page_fillable(

    ui.h2("Crime Trends Dashboard (1975–2015)"),

    ui.layout_sidebar(

        # ---- Sidebar ----
        ui.sidebar(
            ui.input_selectize(
                "city",
                "Select City",
                choices=["New York City", "Chicago", "Los Angeles"],
                multiple=True
            ),

            ui.input_slider(
                "year_range",
                "Year Range",
                min=1975,
                max=2015,
                value=(1975, 2015)
            ),

            ui.input_select(
                "crime_type",
                "Crime Type",
                choices=["Violent Crime", "Property Crime"]
            ),

            ui.input_action_button("reset", "Reset Filters"),
        ),

        # ---- Main content ----
        ui.layout_columns(
            ui.card(
                ui.card_header("Peak Crime Year"),
                "Placeholder: will show peak year."
            ),
            ui.card(
                ui.card_header("Crime Rate"),
                "Placeholder: will show selected crime rate."
            ),
            col_widths=(6, 6),
        ),

        ui.card(
            ui.card_header("Trend Over Time"),
            "Placeholder: Line chart will appear here."
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Map View"),
                "Placeholder: Map visualization."
            ),
            ui.card(
                ui.card_header("City Comparison"),
                "Placeholder: Bar chart comparison."
            ),
            col_widths=(6, 6),
        ),
    ),
)

def server(input, output, session):
    pass

app = App(app_ui, server)
