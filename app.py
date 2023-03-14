import pandas as pd
import plotly.express as px

from pathlib import Path
from dash import Dash, html, dcc


app = Dash(__name__)
app.title = "Twitch viewership"
server = app.server


HISTORY_PATH = Path().absolute() / "history.csv"


def load_data():
    df = pd.read_csv(HISTORY_PATH)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    return df


def serve_layout():
    df = load_data()
    fig = px.line(df, x="date", y="count", title="Concurrent viewers over time")
    fig.update_layout(title_x=0.5)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return html.Div(children=[
        html.H1('Twitch viewership', className="header-title", style={'textAlign': 'center'}),

        html.Div([f"Live viewers now: ", html.B(df['count'].iloc[-1])]),

        dcc.Graph(figure=fig),

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

