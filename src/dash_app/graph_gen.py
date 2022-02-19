import plotly.graph_objects as go
import numpy as np

from mmodel.mmodel import MetaModel
from typing import Dict


def show_simulation(model: MetaModel, result: Dict, time: np.ndarray):
    cmodel = get_compartimental_model_type(model).lower()
    if cmodel in {"sir", "sirs"}:
        return show_sir_simulation(model, result, time)

    if cmodel == "sis":
        return show_sis_simulation(model, result, time)

    raise NotImplementedError(f"No visualization for {cmodel} compartimental models")


def show_sir_simulation(model: MetaModel, result: Dict, time: np.ndarray):
    s, i, r = (0, 0, 0)
    for node in model.network.nodes:
        idx = node.id
        s += result[idx]["S"]
        i += result[idx]["I"]
        r += result[idx]["R"]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=time, y=s, mode="lines", name="S"))
    figure.add_trace(go.Scatter(x=time, y=i, mode="lines", name="I"))
    figure.add_trace(go.Scatter(x=time, y=r, mode="lines", name="R"))

    return figure


def show_sis_simulation(model: MetaModel, result: Dict, time: np.ndarray):
    s, i = 0, 0
    for node in model.network.nodes:
        idx = node.id
        s += result[idx]["S"]
        i += result[idx]["I"]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=time, y=s, mode="lines", name="S"))
    figure.add_trace(go.Scatter(x=time, y=i, mode="lines", name="I"))
    return figure


def get_compartimental_model_type(model: MetaModel) -> str:
    return model.network.nodes[0].cmodel
