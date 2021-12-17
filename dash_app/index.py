import dash
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from app import app
from dash_app import models
# navigation bar of the application
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                "Models",
                href='/models'
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
    id='cytoscape-two-nodes',
    layout={'name':'preset'},
    style={'width':'100%', 'height':'400px'},
    elements = [
        {'data' : {'id':'one', 'label':'Node1'}, 'position':{'x':75, 'y':75}},
        {'data' : {'id':'two', 'label':'Node2'}, 'position':{'x':200, 'y':200}},
        {'data' : {'source': 'one', 'target': 'two'}}
    ])

# a plot to show the behaviour of the pandemic 
network_graph = dcc.Graph()

# groups the network related components
network_graphs = dbc.Row([
    dbc.Col([network],
        sm=12,
        md=6),
    dbc.Col([network_graph],
        sm=12,
        md=6)
    ])

# a plot to show the behaviour of the pandemic in a specific node
node_graph = dcc.Graph()

node_graphs = dbc.Row([
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Model description
            _____
            This will show the description of the model used at the selected node
            """),
        node_graph],
        sm=12,
        md=6),
    dbc.Col([
        dcc.Markdown(
            f"""
            -----
            ##### Model features
            _____
            Here will be controls to adjust the selected node model features""")
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
            """)
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
        network_info, network_graphs, node_graphs])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar, html.Div(id='page-content') 
   ])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/models':
        return models.layout
    else:
        return layout

if __name__ == '__main__':
    app.run_server(debug=True)
            
