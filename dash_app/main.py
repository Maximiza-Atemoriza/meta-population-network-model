import dash
import importlib
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State
from metapopulation_network_model.compile import compile_model
from io import BytesIO
import base64

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])
app.config.suppress_callback_exceptions = True

model_example = r"""
\frac{dS}{dt} = - \frac{\beta S I}{N}\\
\frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I\\
\frac{dR}{dt} = \gamma I
"""
model_name_example = "ModelSIR"

controls = html.Div(
    [
        html.Div(
            id="controls-div",
            children=[
                html.H4(children=[dbc.Label("Model Name")]),
                dbc.Input(id="model-name", type="text"),
                html.H4(children=[dbc.Label("Model in Latex")]),
                dbc.Textarea(id="model-text-area", rows="4"),
                dbc.Button(id="button-model", type="submit", children="Generate Model"),
            ],
        ),
        html.Div(id="params-div"),
    ]
)

app.layout = dbc.Container(
    [
        html.H1("Epidemological Models Generator"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(html.Div(id="model-graph", children=[dcc.Graph()]), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("params-div", "children"),
    Input("button-model", "n_clicks"),
    State("model-name", "value"),
    State("model-text-area", "value"),
)
def generate_model(n_clicks, model_name, model_latex):
    if not model_latex or not model_name:
        return ""
    if n_clicks is not None:
        compile_model(model_latex, model_name)
        module = importlib.import_module(
            f"metapopulation_network_model.models.{model_name}"
        )
        model = getattr(module, model_name)
        result = html.Div(id="params-controls")
        result.children = []
        for param in model.params + model.sets:
            result.children.append(
                html.Div(
                    children=[
                        dbc.Label(children=f"{param}"),
                        dbc.Input(id=f"{param}-input", type="text"),
                    ]
                )
            )

        result.children.append(
            dbc.Button(id="button-graph", type="submit", children="Generate Graph"),
        )
        return result


@app.callback(
    Output("model-graph", "children"),
    Input("button-graph", "n_clicks"),
    State("params-controls", "children"),
    State("model-name", "value"),
)
def generate_graph(n_clicks, children, model_name):
    if n_clicks is not None:
        params = []
        for child in children:
            if child["type"] == "Div":
                params.append(float(child["props"]["children"][1]["props"]["value"]))

        module = importlib.import_module(
            f"metapopulation_network_model.models.{model_name}"
        )
        model = getattr(module, model_name)

        t = np.linspace(0, 160, 160)
        params_count = len(model.params)

        y0 = params[params_count:]
        ret = model.solve(y0, t, tuple(params[:params_count]))
        S, I, R = ret.T

        fig = plt.figure(facecolor="w")
        ax = fig.add_subplot(111, facecolor="#dddddd", axisbelow=True)
        ax.plot(t, S / 1000, "b", alpha=0.5, lw=2, label="Susceptible")
        ax.plot(t, I / 1000, "r", alpha=0.5, lw=2, label="Infected")
        ax.plot(t, R / 1000, "g", alpha=0.5, lw=2, label="Recovered with immunity")
        ax.set_xlabel("Time /days")
        ax.set_ylabel("Number (1000s)")
        ax.set_ylim(0, 1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which="major", c="w", lw=2, ls="-")
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ("top", "right", "bottom", "left"):
            ax.spines[spine].set_visible(False)
        # plt.show()
        plt.savefig("a.png")
        print(params)
        out_url = fig_to_uri(fig)
        result = html.Div([html.Img(id="cur_plot", src=f"{out_url}")], id="plot_div")
        return result


def fig_to_uri(in_fig, close_all=True, **save_args):
    out_img = BytesIO()
    in_fig.savefig(out_img, format="png", **save_args)
    if close_all:
        in_fig.clf()
        plt.close("all")
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)


if __name__ == "__main__":
    app.run_server(debug=True)
