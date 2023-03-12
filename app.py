# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


app = Dash(__name__)
server = app.server


def serve_layout():
    df = pd.read_csv("./history.csv")
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    fig = px.line(df, x="date", y="count")

    return html.Div(children=[
        html.H1('Twitch viewership'),

        html.Div(f"Live viewers now: {df['count'].iloc[-1]}"),

        dcc.Graph(
            id='view-count',
            figure=fig
        )
    ])


app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(debug=True)

