import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px


app = dash.Dash()

app.layout = html.Div(
    id="parent",
    children=[
        html.H1(
            id="H1",
            children="Testing",
            style={"textAlign": "center", "marginTop": 40, "marginBottom": 40},
        ),
    ],
)

if __name__ == "__main__":
    app.run_server()
