#--------------- Dash components ------------------
import dash
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
#------------------- Ploting ----------------------
import plotly.graph_objects as go
import numpy as np
#------------------- Meta Models ------------------
from mmodel.flux import FluxMetaModel
from app import app

FLUX = 1
SIMPLE_TRIP = 2

model = None
application_info = dbc.Row(
    dbc.Col(
        dcc.Markdown("""
            -----
            ### Meta Population Network Models for COVID-19
            -----
            Add here description of the project...

            ...

            ...

            ...


            To start introduce the path to the network file in the input below.
            """
        ), sm = 12, md=12
    )
)

model_file_input = dbc.Row([
    dbc.Col(dcc.Dropdown(
        id='model-type',
        options = [
            { 'label' : 'Flux', 'value': FLUX },
            { 'label' : 'Simple Trip', 'value' : SIMPLE_TRIP }
        ],
        placeholder='Meta Model Type'
    ), sm =12, md=2),
    dbc.Col(
        dbc.Input(
            id='input-model', 
            placeholder='path/to/network/file',
            type='text'
        ), 
        sm =12,
        md = 4
    ),
    dbc.Col(
        dbc.Input(
            id='input-model-name',
            placeholder='model_name',
            type='text'
        ),
        sm=12,
        md=2
    ),
    dbc.Col(
        dbc.Button(id='input-model-btn',
            children='Create'
        ),
        sm=12,
        md=3
    ),
    html.Div(id='input-model-result', style={'margin-top':'10px'})
])

network_info = dbc.Row(
    dbc.Col(
        dcc.Markdown(
            """
            -----
            ##### Network Description
            _____
            Here will be a description of the network being used
            """
        ), sm = 12, md = 12)
)

# The network graph representation
network_graph = cyto.Cytoscape(
    id='cytoscape-network',
    layout = {'name':'cose'},
    style= {'width':'100%', 'height':'400px'},
    elements = [],
    stylesheet = [
        {   'selector' : 'node',
            'style' : {
                'label' : 'data(label)'
            }
        },
        {
            'selector' : 'edge',
            'style' : {
                'curve-style': 'bezier',
                'target-arrow-shape': 'vee',
            }
        }
    ]
)

# The network simulation line chart
network_chart = dcc.Graph()

network_visualization = dbc.Row([
    dbc.Col(network_graph, sm=12, md=6),
    dbc.Col(network_chart, sm=12, md=6)
])

layout = dbc.Container([application_info, model_file_input, network_info, network_visualization])

@app.callback(
    Output('input-model-result', 'children'),
    Output('cytoscape-network', 'elements'),
    Input('input-model-btn', 'n_clicks'),
    State('input-model', 'value'),
    State('input-model-name', 'value'),
    State('model-type', 'value'),
    prevent_initial_call=True
)
def load_input_model(n_clicks, file_path, model_name, model_type):
    if model_type == FLUX:
        model = FluxMetaModel(model_name, file_path)
        alert = dbc.Col(dbc.Alert('Meta Model loaded successfuly', color = 'success', dismissable=True), md=10)
        elements = []
        for node in model.network.nodes:
            elements.append({ 'data' : { 
                'id': str(node.id), 
                'label': node.label }})
        for edge in model.network.edges:
            elements.append({ 'data' : { 
                'source' : str(edge.source), 
                'target' : str(edge.target),
            }})
        return alert, elements
    return None, []
