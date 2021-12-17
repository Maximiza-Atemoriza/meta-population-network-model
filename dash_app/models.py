import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from app import app

model_definition = dbc.Col([
    dcc.Markdown(
        f"""
        -----
        ### Compartmental model definition
        -----
        This section will guide you through the set up of a model that can be used in a network
        simulation. If you already have set up your model this section can also be used to modify
        or delete any existent model."""),
    dcc.Markdown(
        f"""
        -----
        ##### Setting the model's name
        -----
        Here you can set a name for your model.
        For example it can be:
        *\" SIR model with vaccination schema \"*
        """),
    dcc.Input(value='Your model\'s name', type='text', size='129'),
    dcc.Markdown("""
    Are you searching for an existent model? Use this."""),
    dcc.Dropdown(
        id='selected-model',
        options = [
            {'label': 'No Model', 'value':0},
            {'label': 'SIR Model', 'value': 1},
            {'label': 'SIRS Model', 'value': 2}
        ],
        value=0),
    dcc.Markdown(
        f"""
        -----
        ##### Add a general description for your model
        -----
        Here you can explain about what is your model intended for so you can easily know in what situations apply it later"""),
    dcc.Textarea(
        id='input-model-description',
        value='Insert here your model\'s description',
        style={'width': '100%', 'height':200},
        draggable=False),
    dcc.Markdown(
        f"""
        -----
        ##### Add a description for the model\'s features
        -----
        Here you can give a description for the sets and parameteres that are used in the model. You can explain what represent each set, parameter and add any information that you consider relevant for the understanding of the model.
        """),
    dcc.Textarea(
        id='input-features-description',
        value='Insert here your model parameter\'s description',
        style={'width': '100%', 'height':200},
        draggable=False),
    dcc.Markdown(
        f"""
        -----
        ##### Add the system of equations
        -----
        The most important part. You can add your system of equations by just copying the equations in latex format.
        """),
    dcc.Textarea(
        id='input-model-equations',
        value='Insert here your model\'s equations',
        style={'width':'100%', 'height':200},
        draggable=False),
    dcc.Markdown(
        """
        Your model is ready to compile, just click the button"""),
#    dbc.Row([
        html.Button('Compile', id='compile-btn'),
        html.Button('Delete', id='delete-btn'),
        dcc.Markdown(
                """After you compiled your model this will become available for the network simulations""")

],md=8)

body_layout = dbc.Container([
    dbc.Row([model_definition],
        justify='center')], fluid=True)

layout = html.Div([body_layout])
