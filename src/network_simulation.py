# --------------- Dash components ------------------
from functools import reduce
from typing import Dict, Union
import dash
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

# ------------------- Ploting ----------------------
import plotly.graph_objects as go
import numpy as np

# ------------------- Meta Models ------------------
from mmodel.flux import FluxMetaModel
from app import app
from mmodel.mmodel import MetaModel

FLUX = 1
SIMPLE_TRIP = 2

LOAD = 1
GENERATE = 2

model: Union[MetaModel, None] = None
result: Union[Dict, None] = None

application_info = dbc.Row(
    dbc.Col(
        dcc.Markdown(
            """
            -----
            ### Meta Population Network Models for COVID-19
            -----
            Start by filling each parameter field.

            **Network Configuration**  stablish node topology and edge weight:
            * _Meta Model_ sets the type of the meta model
            * _path/to/network/file_ load the network configuration from the indicated file
            * _Model Name_ is the name used to store the compiled network configuration

            **Network Parameters** stablish each node compartimental model type and its params:
            * If dropdown is equal to _Load_:
                * _path/to/network/params_ loads the parameter of each node from a selected file
            * If dropdown is equal to _Generate_:
                * _path/to/network/params_ generates a file in selected location. It uses xml or json notation depending on filetype.

            **Simulation**
            * _Simulation Time_ sets simulation total duration
            """
        ),
        sm=12,
        md=12,
    )
)

model_file_input = dbc.Row(
    [
        dcc.Markdown("##### Network Configuration"),
        dbc.Col(
            dcc.Dropdown(
                id="model-type",
                options=[
                    {"label": "Flux", "value": FLUX},
                    {"label": "Simple Trip", "value": SIMPLE_TRIP},
                ],
                placeholder="Meta Model Type",
                value=FLUX,
                clearable=True,
                searchable=False,
                persistence=True,
                persistence_type="session",
            ),
            sm=12,
            md=2,
        ),
        dbc.Col(
            dbc.Input(
                id="input-model",
                placeholder="path/to/network/file",
                type="text",
                persistence=True,
                persistence_type="session",
            ),
            sm=12,
            md=4,
        ),
        dbc.Col(
            dbc.Input(
                id="input-model-name",
                placeholder="Model Name",
                type="text",
                persistence=True,
                persistence_type="session",
            ),
            sm=12,
            md=2,
        ),
        dbc.Col(
            dbc.Button(id="input-model-btn", children="Compile", color="primary"),
            sm=12,
            md=3,
        ),
        html.Div(id="input-model-result", style={"marginTop": "10px"}),
    ],
)

param_file_input = dbc.Row(
    [
        dcc.Markdown("##### Network Parameters"),
        dbc.Col(
            dcc.Dropdown(
                id="select-params",
                options=[
                    {"label": "Load", "value": LOAD},
                    {"label": "Generate", "value": GENERATE},
                ],
                value=LOAD,
                clearable=False,
                searchable=False,
                persistence=True,
                persistence_type="session",
            ),
            sm=12,
            md=2,
        ),
        dbc.Col(
            dbc.Input(
                id="input-params",
                placeholder="path/to/network/params",
                type="text",
                persistence=True,
                persistence_type="session",
            ),
            sm=12,
            md=4,
        ),
        dbc.Col(
            dbc.Button(id="generate-params-btn", children="Generate", color="primary"),
            sm=12,
            md=3,
        ),
        html.Div(
            id="param-status",
            style={
                "marginTop": "10px",
            },
        ),
    ]
)

start_simulation = dbc.Row(
    [
        dcc.Markdown("##### Simulation", style={"marginTop": "10px"}),
        dbc.Col(
            dbc.Input(
                id="input-time",
                placeholder="Simulation Time",
                type="number",
                persistence=True,
                persistence_type="session",
            ),
            sm=12,
            md=3,
        ),
        dbc.Col(
            [
                dbc.Button(
                    id="simulate-btn",
                    children="Run Simulation",
                    color="success",
                    style={
                        "paddingRight": "40px",
                        "paddingLeft": "40px",
                        "textStyle": "bold",
                    },
                ),
            ],
            sm=12,
            md=3,
        ),
        html.Div(
            id="simul-status",
            style={
                "marginTop": "10px",
            },
        ),
    ]
)

network_info = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Markdown(
                    f"""
            -----
            ##### Network Geo Graph
            Graphical output of network configuration
            """
                )
            ],
            sm=12,
            md=6,
        ),
        dbc.Col(
            [
                dcc.Markdown(
                    f"""
            -----
            ##### Network Behaviour
            Network behaviour agains time during the simulation
            """
                )
            ],
            sm=12,
            md=6,
        ),
    ]
)


# The network graph representation
network_graph = cyto.Cytoscape(
    id="cytoscape-network",
    layout={"name": "cose"},
    style={"width": "100%", "height": "400px"},
    elements=[],
    stylesheet=[
        {"selector": "node", "style": {"label": "data(label)"}},
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "vee",
            },
        },
    ],
)

# The network simulation line chart
network_chart = dcc.Graph(id="network-chart")

network_visualization = dbc.Row(
    [dbc.Col(network_graph, sm=12, md=6), dbc.Col(network_chart, sm=12, md=6)]
)

node_chart = dcc.Graph(id="node-graph")

node_visualization = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Markdown(
                    f"""
            ----- 
            ##### Node Behaviour
            Visualize a single node's behaviour
            """
                ),
                node_chart,
            ],
            sm=12,
            md=6,
        ),
    ]
)

layout = dbc.Container(
    [
        application_info,
        model_file_input,
        param_file_input,
        start_simulation,
        network_info,
        network_visualization,
        node_visualization,
    ]
)


@app.callback(
    Output("input-model-result", "children"),
    Output("cytoscape-network", "elements"),
    Input("input-model-btn", "n_clicks"),
    State("input-model", "value"),
    State("input-model-name", "value"),
    State("model-type", "value"),
    prevent_initial_call=True,
)
def load_input_model(n_clicks, file_path, model_name, model_type):
    global model
    if model_type == FLUX:
        try:
            model = FluxMetaModel(model_name, file_path)
        except (AttributeError, FileNotFoundError) as err:
            text = "Configuration file is not set." if file_path is None else ""
            text = "File not found." if isinstance(err, FileNotFoundError) else ""
            fail = dbc.Col(
                dbc.Alert(
                    f"Could not load meta-model. {text}",
                    color="warning",
                    dismissable=True,
                ),
                md=10,
            )
            return fail, []
    else:
        fail = dbc.Col(
            dbc.Alert("Invalid Meta-Model type", color="warning", dismissable=True),
            md=10,
        )
        return fail, []

    success = dbc.Col(
        dbc.Alert("Meta-Model loaded successfuly", color="success", dismissable=True),
        md=10,
    )
    elements = []
    for node in model.network.nodes:
        elements.append(
            {
                "data": {
                    "id": str(node.id),
                    "label": node.label,
                    "cmodel": node.cmodel,
                }
            }
        )
    for edge in model.network.edges:
        elements.append(
            {
                "data": {
                    "source": str(edge.source),
                    "target": str(edge.target),
                }
            }
        )
    return success, elements


@app.callback(
    Output("generate-params-btn", "disabled"),
    Output("generate-params-btn", "color"),
    Input("select-params", "value"),
)
def load_or_generate(value):
    if value == LOAD:
        return (True, "secondary")
    return (False, "primary")


@app.callback(
    Output("param-status", "children"),
    Output("select-params", "value"),
    Input("generate-params-btn", "n_clicks"),
    State("input-params", "value"),
    prevent_initial_call=True,
)
def generate_base_model(_, input_params):
    if model is None:
        return (
            dbc.Col(
                dbc.Alert(
                    "Please load a network configuration first.",
                    color="warning",
                    dismissable=True,
                ),
                md=10,
            ),
            GENERATE,
        )
    if not input_params.endswith(".xml") and not input_params.endswith(".json"):
        return (
            dbc.Col(
                dbc.Alert(
                    "Can only generate in xml and json formats.",
                    color="warning",
                    dismissable=True,
                ),
                md=10,
            ),
            GENERATE,
        )

    try:
        model.export_input(input_params)
    except FileNotFoundError:
        return (
            dbc.Col(
                dbc.Alert(
                    "Invalid path to file.",
                    color="warning",
                    dismissable=True,
                ),
                md=10,
            ),
            GENERATE,
        )

    return (
        dbc.Alert(
            "Generation succesfull",
            color="success",
            dismissable=True,
        ),
        LOAD,
    )


@app.callback(
    Output("simul-status", "children"),
    Output("network-chart", "figure"),
    Input("simulate-btn", "n_clicks"),
    State("input-params", "value"),
    State("input-time", "value"),
    prevent_initial_call=True,
)
def simulate_network(_, input_params, input_time):
    if model is None:
        not_yet = dbc.Col(
            dbc.Alert(
                "Please load a network configuration first.",
                color="warning",
                dismissable=True,
            ),
            md=10,
        )
        return not_yet, go.Figure()

    try:
        input_time = np.linspace(0, input_time, input_time)
        global result
        result = model.simulate(input_params, input_time)
    except (TypeError, AttributeError):
        print("simulation failed 1")
        text = "Parameter file is not set." if input_params is None else ""
        text += "\n\nSimulation time is not set." if input_time is None else ""
        not_yet = dbc.Col(
            dbc.Alert(
                f"Please fill a meta-model parameter with valid information.\n\n{text}",
                color="warning",
                dismissable=True,
            ),
            md=10,
        )
        print("exit1")
        return not_yet, go.Figure()

    # Right now it is assumed only sir model is used
    s, i, r = (0, 0, 0)
    for node in model.network.nodes:
        idx = node.id
        s += result[idx]["S"]
        i += result[idx]["I"]
        r += result[idx]["R"]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=input_time, y=s, mode="lines", name="S"))
    figure.add_trace(go.Scatter(x=input_time, y=i, mode="lines", name="I"))
    figure.add_trace(go.Scatter(x=input_time, y=r, mode="lines", name="R"))

    completed = dbc.Col(
        dbc.Alert(
            "Simulation Completed",
            color="success",
            dismissable=True,
        ),
        md=10,
    )
    return completed, figure


@app.callback(
    Output("node-graph", "figure"),
    Input("cytoscape-network", "selectedNodeData"),
    State("input-time", "value"),
    prevent_initial_call=True,
)
def simulate_node(node_data, time):
    print("Call to node show")
    print(node_data)

    try:
        idx = node_data[0]["id"]
    except (IndexError):
        return go.Figure()

    if result is None:
        return go.Figure()

    # Only SIR cmodel is assumed
    print(idx)
    s = result[idx]["S"]
    i = result[idx]["I"]
    r = result[idx]["R"]

    time = np.linspace(0, time, time)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=time, y=s, mode="lines", name="S"))
    figure.add_trace(go.Scatter(x=time, y=i, mode="lines", name="I"))
    figure.add_trace(go.Scatter(x=time, y=r, mode="lines", name="R"))

    print("returning calculated figure")
    return figure
