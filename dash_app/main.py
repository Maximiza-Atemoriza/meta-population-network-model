import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

badge = dbc.Button(id='button',
    children=[
        
        "Notifications",
        dbc.Badge("4", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

# Then we incorporate the snippet into our layout.
# This example keeps it simple and just wraps it in a Container
app.layout = dbc.Container(badge, fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
