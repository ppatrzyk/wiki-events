from dash import Dash, html, dcc
import db

def _get_fig_data():
    """
    Query and format data for figures
    """
    figures = dict()
    # wiki_hourly_summary
    wiki_hourly_summary = db.execute("select * from wiki_hourly_summary order by interval asc")
    figures["wiki_hourly_summary"] = {
        "data": [
            {"x": wiki_hourly_summary.get("interval"), "y": wiki_hourly_summary.get("events"), "type": "line", "name": "Hourly count"},
        ],
        "layout": {
            "title": "Wiki hourly summary"
        }
    }
    
    # wiki_minutely_summary
    wiki_minutely_summary = db.execute("select * from wiki_minutely_summary order by interval asc")
    figures["wiki_minutely_summary"] = {
        "data": [
            {"x": wiki_minutely_summary.get("interval"), "y": wiki_minutely_summary.get("events"), "type": "line", "name": "Minutely count"},
        ],
        "layout": {
            "title": "Wiki minutely summary"
        }
    }

    # wiki_hourly_bywiki_summary
    # TODO

    # wiki_minutely_bywiki_summary
    # TODO

    # wiki_weekdays_summary
    # TODO picker for wiki
    wiki_weekdays_summary = db.execute("select * from wiki_weekdays_summary where wiki_name == 'plwiki'")
    figures["wiki_weekdays_summary"] = {
        "data": [
            {"x": wiki_weekdays_summary.get("hour"), "y": wiki_weekdays_summary.get("weekday"), "z": wiki_weekdays_summary.get("events"), "type": "heatmap", "name": "Week heatmap"},
        ],
        "layout": {
            "title": "Weekly heatmap"
        }
    }

    # wiki_bywiki_summary
    wiki_bywiki_summary = db.execute("select * from wiki_bywiki_summary order by events desc limit 20")
    figures["wiki_bywiki_summary"] = {
        "data": [
            {"x": wiki_bywiki_summary.get("wiki_name"), "y": wiki_bywiki_summary.get("events"), "type": "bar", "name": "Total events"},
        ],
        "layout": {
            "title": "Total events by wiki (top 20)"
        }
    }

    # wiki_event_types
    wiki_event_types = db.execute("select * from wiki_event_types order by event_type, bot")
    figures["wiki_event_types"] = {
        "data": db.groupby_traces(wiki_event_types, "bot", "event_type", "events", "bar"),
        "layout": {
            "title": "Total events by wiki (top 20)"
        }
    }
    return figures

def _render_layout():
    """
    Generate dash page
    """
    figures = _get_fig_data()
    layout = html.Div([
        # html.Div(children=str(data)),
        dcc.Graph(figure=figures.get("wiki_minutely_summary")),
        dcc.Graph(figure=figures.get("wiki_hourly_summary")),
        dcc.Graph(figure=figures.get("wiki_weekdays_summary")),
        dcc.Graph(figure=figures.get("wiki_bywiki_summary")),
        dcc.Graph(figure=figures.get("wiki_event_types")),
    ])
    return layout

app = Dash(__name__)
app.layout = _render_layout
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
