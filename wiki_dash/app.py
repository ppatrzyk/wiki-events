from dash import Dash, html, dcc, Input, Output, callback
import db
import plotly

LAYOUT_COMMON = {
      "font": {"size": 16, "family": "system-ui, sans-serif"},
      "template": plotly.io.templates["ggplot2"],
}

def _get_static_fig_data():
    """
    Query and format data for visualization
    """
    fig_data = dict()
    # wiki_hourly_summary
    wiki_hourly_summary = db.execute(operation="select * from wiki_hourly_summary order by interval asc")
    fig_data["wiki_hourly_summary"] = {
        "data": [
            {"x": wiki_hourly_summary.get("interval"), "y": wiki_hourly_summary.get("events"), "type": "line", "name": "Hourly count"},
        ],
        "layout": {
            "title": "Total hourly events", **LAYOUT_COMMON
        }
    }
    
    # wiki_minutely_summary
    wiki_minutely_summary = db.execute(operation="select * from wiki_minutely_summary order by interval asc")
    fig_data["wiki_minutely_summary"] = {
        "data": [
            {"x": wiki_minutely_summary.get("interval"), "y": wiki_minutely_summary.get("events"), "type": "line", "name": "Minutely count"},
        ],
        "layout": {
            "title": "Total minutely events", **LAYOUT_COMMON
        }
    }

    # wiki_bywiki_summary
    wiki_bywiki_summary = db.execute(operation="select * from wiki_bywiki_summary order by events desc limit 20")
    fig_data["wiki_bywiki_summary"] = {
        "data": [
            {"x": wiki_bywiki_summary.get("wiki_name"), "y": wiki_bywiki_summary.get("events"), "type": "bar", "name": "Total events"},
        ],
        "layout": {
            "title": "Total events by wiki (top 20)", **LAYOUT_COMMON
        }
    }

    # unique wiki_name list
    wiki_names = db.execute(operation="select distinct(wiki_name) as wiki_name from wiki_weekdays_summary order by wiki_name asc")
    fig_data["wiki_names"] = wiki_names.get("wiki_name")

    return fig_data

def _get_bywiki_fig_data(wiki):
    """
    Query and format bywiki data for visualization
    """
    fig_data = dict()
    # wiki_hourly_bywiki_summary
    wiki_hourly_bywiki_summary = db.execute(
        operation="select * from wiki_hourly_bywiki_summary where wiki_name == %(wiki)s order by interval asc",
        parameters={"wiki": wiki}
    )
    fig_data["wiki_hourly_bywiki_summary"] = {
        "data": [
            {"x": wiki_hourly_bywiki_summary.get("interval"), "y": wiki_hourly_bywiki_summary.get("events"), "type": "line", "name": wiki},
        ],
        "layout": {
            "title": f"Hourly events ({wiki})", **LAYOUT_COMMON
        }
    }

    # wiki_minutely_bywiki_summary
    wiki_minutely_bywiki_summary = db.execute(
        operation="select * from wiki_minutely_bywiki_summary where wiki_name == %(wiki)s order by interval asc",
        parameters={"wiki": wiki}
    )
    fig_data["wiki_minutely_bywiki_summary"] = {
        "data": [
            {"x": wiki_minutely_bywiki_summary.get("interval"), "y": wiki_minutely_bywiki_summary.get("events"), "type": "line", "name": wiki},
        ],
        "layout": {
            "title": f"Minutely events ({wiki})", **LAYOUT_COMMON
        }
    }

    # wiki_weekdays_summary
    wiki_weekdays_summary = db.execute(
        operation="select * from wiki_weekdays_summary where wiki_name == %(wiki)s order by weekday, hour asc",
        parameters={"wiki": wiki}
    )
    fig_data["wiki_weekdays_summary"] = {
        "data": [
            {"x": wiki_weekdays_summary.get("hour"), "y": wiki_weekdays_summary.get("weekday"), "z": wiki_weekdays_summary.get("events"), "type": "heatmap", "name": "Week heatmap"},
        ],
        "layout": {
            "title": f"Weekly heatmap ({wiki})", **LAYOUT_COMMON
        }
    }
    return fig_data

def _render_layout():
    """
    Generate dash page
    """
    static_fig_data = _get_static_fig_data()
    layout = html.Div([
        dcc.Markdown("*intro content*"),
        dcc.Graph(figure=static_fig_data.get("wiki_minutely_summary")),
        dcc.Graph(figure=static_fig_data.get("wiki_hourly_summary")),
        dcc.Graph(figure=static_fig_data.get("wiki_bywiki_summary")),
        html.Div([
            dcc.Markdown("*intro content*"),
            dcc.Dropdown(static_fig_data.get("wiki_names"), 'plwiki', id='wiki-name-dropdown'),
        ]),
        dcc.Graph(id='wiki_minutely_bywiki_summary'),
        dcc.Graph(id='wiki_hourly_bywiki_summary'),
        dcc.Graph(id='wiki_weekdays_summary'),
    ])
    return layout

app = Dash(__name__)
app.layout = _render_layout
server = app.server

@callback(
    Output('wiki_minutely_bywiki_summary', 'figure'),
    Output('wiki_hourly_bywiki_summary', 'figure'),
    Output('wiki_weekdays_summary', 'figure'),
    Input('wiki-name-dropdown', 'value')
)
def update_output(wiki):
    bywiki_fig_data = _get_bywiki_fig_data(wiki)
    return bywiki_fig_data.get("wiki_minutely_bywiki_summary"), bywiki_fig_data.get("wiki_hourly_bywiki_summary"), bywiki_fig_data.get("wiki_weekdays_summary")

if __name__ == "__main__":
    app.run(debug=True)
