import dash
import importlib
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from app import app
from dash_app import add_model
from repository import ModelRepository
from metapopulation_network_model.models.graph_models.simple import SimpleGraph
import plotly.graph_objects as go
import numpy as np

nodes = {
        'one': {'id':'one', 'label':'Node1', 'model': 0, 'initial-conditions':None, 'parameters':None, 'result':None},
    'two': {'id':'two', 'label':'Node2', 'model': 0, 'initial-conditions':None, 'parameters':None, 'result':None}
}
edges = [{'source':'one', 'target':'two', 'weigth_source':0.8, 'weigth_target':0.1}]

sim_result = go.Figure()
# ===================================== Layout ===============================================

# navigation bar 
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                "Models",
                href='/add_model'
            )
        )
    ],
    brand='Metapopulation network models for COVID-19',
    brand_href='/',
    color='dark',
    dark=True,
)

# this row shows to the left the model description and to the right the model features description
network_info = dbc.Row([
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Network description:
            -----
            For this demonstration we will use a simple connected network of two nodes
            """)
        ],
        sm=12,
        md=6
    ),
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Network features:
            -----
            Some features of the model
            """)
        ],
        sm=12,
        md=6
    )
])

# the network graph 
network = cyto.Cytoscape(
    id='cytoscape-network',
    layout={'name':'cose'},
    style={'width':'100%', 'height':'400px'},
    elements= [{ 'data': data } for data in list(nodes.values()) + edges]
)

# a plot to show the behaviour of the pandemic 
network_graph = dcc.Graph(id='network-graph')

# groups the network related components
network_graphs = dbc.Row([
    dbc.Col([network],
        sm=12,
        md=6),
    dbc.Col([network_graph],
        sm=12,
        md=6),
    ])

# a plot to show the behaviour of the pandemic in a specific node
node_graph = dcc.Graph(id='node-graph')

node_graphs = dbc.Row([
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Model description
            _____
            This will show the description of the model used at the selected node
            """),
        dcc.Dropdown(
            id='node-selected-model',
            options = [ {'label':'No Model', 'value':0}, {'label':'SIR Model', 'value':'SIR'}],
            value=0),
        html.Button(
            id='update-models-dropdown-btn',
            style={'display':'none'}),
        node_graph],
        sm=12,
        md=6),
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Model features
            _____
            Here will be controls to adjust the selected node model features"""),
        html.Div(id='node-model-features', style={'margin':'10px'}),
        dbc.Row([
            dbc.Button(children='Set model', id='set-model-btn'),
        ]),
        html.Div(id='set-features-result', style={'margin':'10px'})
        ],
        sm=12,
        md=3),
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Edge features
            -----
            Here will be controls to adjust the selected edge features
            """),
        dbc.Row(
            children=[
                dbc.Col([dbc.Label(children=f"Node1")], md=5),
                dbc.Col([dbc.Input(id=f"node1-weigth", type="text")], md=7)
            ], style={'margin':'15px'}
        ),
        dbc.Row(
            children=[
                dbc.Col([dbc.Label(children=f"Node2")], md=5),
                dbc.Col([dbc.Input(id=f"node2-weigth", type="text")], md=7)
            ], style={'margin':'15px'}
        ),
        dbc.Button('Set edge', id='set-edge-btn'),
        html.Div(id='set-edge-result'),
        html.Button(id='refresh-edge-btn', style={'display':'None'})
        ],
        sm=12,
        md=3)
])

layout = dbc.Container([
    dcc.Markdown(
        f"""
        -----
        ### Network simulation
        -----
        This section provides a framework for developing and testing metapopulation network models 
        for research purposes. Add the objectives of the project here. 
        """),
    dbc.Button('Simulate', id='simulate-btn'),
    network_info,
    network_graphs,
    node_graphs])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar, html.Div(id='page-content') 
   ])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/add_model':
        return add_model.layout
    else:
        return layout
 

# ================================== Callbacks =======================================
@app.callback(
    Output('node-model-features', 'children'),
    Output('node-selected-model', 'value'),
    Output('node-graph', 'figure'),
    Input('cytoscape-network', 'selectedNodeData'),
    Input('node-selected-model', 'value'),
    prevent_initial_call=True
)
def display_node_model(node_data, selected_model):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if not node_data:
        return 'No node is selected', 0, go.Figure()
    else:
        idx = node_data[0]['id']
        label = nodes[idx]['label'] 
        content = f'Node {label} was selected\n'
        if input_id == 'cytoscape-network':
            content += 'It was changed the current selected node\n'
            selected_model = nodes[idx]['model']
        else:
            content += 'It was changed the selected model\n'
        if not selected_model:
            content += 'No model is selected'
        else:
            content = get_model_features_components(selected_model, nodes[idx])
        return content,selected_model, get_figure(idx)
def get_figure(idx):
    node = nodes[idx]
    fig = go.Figure()
    if not node['result']:
        return fig
    S,I,R = node['result']
    t = np.linspace(0,160, 160)
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='S'))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='I'))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='R'))
    return fig 

def get_model_features_components(model_name, node):
    module = importlib.import_module(f'metapopulation_network_model.models.{model_name}')
    model = getattr(module, model_name)
    model_features = model.params + model.sets

    node_features = [""] * len(model_features)
    if model_name == node['model']:
        node_features = [str(f) for f in node['parameters'] + node['initial-conditions']]
    result = html.Div(id="params-controls", style={'overflow':'scroll'})
    result.children = []
    for feat, value in zip(model_features, node_features):
        result.children.append(
            dbc.Row(
                children=[
                    dbc.Col([dbc.Label(children=f"{feat}")], md=5),
                    dbc.Col([dbc.Input(id=f"{feat}-input", type="text", value=value)], md=7)
                    ], style={'margin':'15px'}
            )
        )
    return result

@app.callback(
    Output('set-features-result', 'children'),
    Input('set-model-btn', 'n_clicks'),
    State('cytoscape-network', 'selectedNodeData'),
    State('node-selected-model', 'value'),
    State('node-model-features', 'children'),
    prevent_initial_call=True
)
def set_model(n_clicks, selected_node, model_name, features_group):
    if not selected_node:
        return 'You have not selected a node'
    if not model_name:
        return 'You have not selected a model for this node'

    # get features values from the control group
    features_group = features_group['props']['children']
    features = []
    for row in features_group:
        col = row['props']['children'][1]
        try:
            features.append(float(col['props']['children'][0]['props']['value']))
        except KeyError:
            return f'You must provide a value for all parameters'

    module = importlib.import_module(f'metapopulation_network_model.models.{model_name}')
    model = getattr(module, model_name)
    params_count = len(model.params)

    idx = selected_node[0]['id']
    nodes[idx]['model'] = model_name
    nodes[idx]['initial-conditions'] = features[params_count:]
    nodes[idx]['parameters'] = features[:params_count]
    return 'Model was set up correctly'

@app.callback(
    Output('network-graph', 'figure'),
    Input('simulate-btn', 'n_clicks')
)
def simulate_network(n_clicks):
    global sim_result
    node1 = nodes['one']
    node2 = nodes['two']
    if not node1['initial-conditions'] or not node1['parameters']:
        return sim_result 
    if not node2['initial-conditions'] or not node2['parameters']:
        return sim_result
    y0 = node1['initial-conditions'] + node2['initial-conditions']
    params = node1['parameters'] + node2['parameters']
    t = np.linspace(0,160,160)

    module = importlib.import_module(f'metapopulation_network_model.models.SIR')
    model = getattr(module, 'SIR')

    f = [[0, edges[0]['weigth_source']], [edges[0]['weigth_target'], 0]]

    network = SimpleGraph(model, f)

    ret = network.solve(y0, t, params)

    S1, I1, R1, S2, I2, R2 = ret.T
    
    node1['result'] = S1, I1, R1
    node2['result'] = S2, I2, R2

    S = S1 + S2
    I = I1 + I2
    R = R1 + R2 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='S'))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='I'))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='R'))
    sim_result = fig
    return fig

@app.callback(
        Output('set-edge-result', 'children'),
        Input('set-edge-btn', 'n_clicks'),
        State('node1-weigth', 'value'),
        State('node2-weigth', 'value'),
        prevent_initial_call=True
)
def set_edge(n_clicks, value1, value2):
    edges[0]['weigth_source'] = float(value1)
    edges[0]['weigth_target'] = float(value2)

@app.callback(
        Output('node1-weigth', 'value'),
        Output('node2-weigth', 'value'),
        Input('cytoscape-network', 'tapEdgeData')
        #Input('refresh-edge-btn', 'n_clicks')
)
def display_edge_weigths(nclicks):
    return edges[0]['weigth_source'], edges[0]['weigth_target']

def update_node_graph(n_clicks, selected_node, figure):
    if not selected_node:
        return figure

    idx = selected_node[0]['id']
    node = nodes[idx]
    node_model = node['model']

    module = importlib.import_module(f'models.{node_model}')
    model = getattr(module, node_model)

    t = np.linspace(0,160, 160)
    y0 = node['initial-conditions']
    params = tuple(node['parameters'])
    ret = model.solve(y0, t, params)
    fig = go.Figure()
    for s in ret.T:
        fig.add_trace(go.Scatter(x=t, y=s, mode='lines'))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
