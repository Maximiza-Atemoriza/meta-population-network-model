import dash
import dash_bootstrap_components as dbc
from repository import ModelRepository
from app import app
from dash import Input, Output, State, dcc, html

model_definition = dbc.Col(
    [
        dcc.Markdown(
            f"""
        -----
        ### Compartmental model definition
        -----
        This section will guide you through the set up of a model that can be used in a network
        simulation. If you already have set up your model this section can also be used to modify
        or delete any existent model."""
        ),
        dcc.Markdown(
            f"""
        -----
        ##### Setting the model's name
        -----
        Here you can set a name for your model.
        For example it can be:
        *\" SIR model with vaccination schema \"*
        """
        ),
        dcc.Input(
            id="input-model-name", value="Your model's name", type="text", size="129"
        ),
        dcc.Markdown("""Are you searching for an existent model? Use this."""),
        dcc.Dropdown(
            id="selected-model",
            options=[
                {"label": "No Model", "value": 0},
            ]
            + [
                {"label": model, "value": model}
                for model in ModelRepository.get_model_names()
            ],
            value=0,
        ),
        dcc.Markdown(
            f"""
        -----
        ##### Add a general description for your model
        -----
        Here you can explain about what is your model intended for so you can easily know in what situations apply it later"""
        ),
        dcc.Textarea(
            id="input-model-description",
            value="Insert here your model's description",
            style={"width": "100%", "height": 200},
            draggable=False,
        ),
        dcc.Markdown(
            f"""
        -----
        ##### Add a description for the model\'s features
        -----
        Here you can give a description for the sets and parameteres that are used in the model. You can explain what represent each set, parameter and add any information that you consider relevant for the understanding of the model.
        """
        ),
        dcc.Textarea(
            id="input-model-features",
            value="Insert here your model parameter's description",
            style={"width": "100%", "height": 200},
            draggable=False,
        ),
        dcc.Markdown(
            f"""
        -----
        ##### Add the system of equations
        -----
        The most important part. You can add your system of equations by just copying the equations in latex format.
        """
        ),
        dcc.Textarea(
            id="input-model-equations",
            value="Insert here your model's equations",
            style={"width": "100%", "height": 200},
            draggable=False,
        ),
        dcc.Markdown(
            """
        Your model is ready to compile, just click the button"""
        ),
        html.Button("Compile", id="compile-btn"),
        html.Button("Delete", id="delete-btn"),
        dcc.Markdown(
            """After you compiled your model this will become available for the network simulations"""
        ),
        html.Div(id="compilation-result"),
    ],
    md=8,
)

body_layout = dbc.Container([dbc.Row([model_definition], justify="center")], fluid=True)

layout = html.Div([body_layout])

# ======================== Callbacks ===========================
@app.callback(
    Output("compilation-result", "children"),
    Input("compile-btn", "n_clicks"),
    State("input-model-name", "value"),
    State("input-model-description", "value"),
    State("input-model-features", "value"),
    State("input-model-equations", "value"),
    prevent_initial_call=True,
)
def compile_model(n_clicks, name, description, features, equations):
    ModelRepository.add_model(name, description, features, equations)
    return "Compiled model"


@app.callback(
    Output("input-model-name", "value"),
    Output("input-model-description", "value"),
    Output("input-model-features", "value"),
    Output("input-model-equations", "value"),
    Output("selected-model", "options"),
    Input("selected-model", "value"),
)
def view_model(selected_model):
    if not selected_model:
        return (
            "Your model's name here",
            "Insert here your model's description",
            "Insert here your model's features descriptions",
            "Insert here your model's equations",
            [{"label": "No Model", "value": 0}]
            + [
                {"label": model, "value": model}
                for model in ModelRepository.get_model_names()
            ],
        )
    else:
        model = ModelRepository.get_model(selected_model)
        return (
            selected_model,
            model["description"],
            model["features"],
            model["equations"],
            [{"label": "No Model", "value": 0}]
            + [
                {"label": model, "value": model}
                for model in ModelRepository.get_model_names()
            ],
        )


@app.callback(
    Output("selected-model", "value"),
    Input("delete-btn", "n_clicks"),
    State("selected-model", "value"),
)
def delete_model(n_clicks, model_name):
    if model_name:
        ModelRepository.remove_model(model_name)
    return 0
