
import pytz
import datetime
import plotly.express as px
import pandas as pd

from pathlib import Path
from datetime import datetime, timedelta, time
from functools import lru_cache
from dash import Dash, html, dcc
from flask_caching import Cache


app = Dash(__name__)
app.title = "Twitch viewership"
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
server = app.server


HISTORY_PATH = Path().absolute() / "history.csv"

@cache.memoize(timeout=5*60)
def load_data():
    df = pd.read_csv(HISTORY_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["timestamp"] = df["timestamp"].dt.tz_localize(pytz.utc)
    df["timestamp"] = df["timestamp"].dt.tz_convert(pytz.timezone("Europe/Paris"))
    df = df.set_index("timestamp")
    return df


@lru_cache(maxsize=1)
def compute_24h_report_metrics(date: datetime):
    df = load_data()
    end = date
    begin = end - timedelta(days=1)

    daily_df = df.loc[begin:end]
    return {
        "maximum": daily_df["count"].max(),
        "mean": round(daily_df["count"].mean())
    }


def serve_layout():
    df = load_data()
    fig = px.line(df, y="count", title="Concurrent viewers over time")
    fig.update_layout(title_x=0.5)
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    daily_report_datetime = datetime.combine(datetime.today(), time(20, 0, 0))
    if datetime.now() < daily_report_datetime:
        daily_report_datetime -= timedelta(days=1)
    daily_report = compute_24h_report_metrics(daily_report_datetime)

    return html.Div(children=[
        html.H1('Twitch viewership', className="header-title", style={'textAlign': 'center'}),

        html.Div([f"Live viewers now: ", html.B(df['count'].iloc[-1])]),

        dcc.Graph(figure=fig),

        html.Div([
            html.H3(f"Last 24h report (generated at {daily_report_datetime})"),
            html.Ul([
                html.Li([f"Avg. Viewers: ", html.B(daily_report["mean"])]),
                html.Li([f"Max. Viewers: ", html.B(daily_report["maximum"])]),
            ])
        ]),

        html.Footer(
            html.I([
                'Website made by Pierre CAILLON. Data scraped from ',
                html.A("TwitchTracker", href="https://twitchtracker.com"),
                '. View source code on ',
                html.A("GitHub", href="https://github.com/pierrecaillon/twitch_viewers"),
                '.',
            ])
        ),
    ])


app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(debug=True)
