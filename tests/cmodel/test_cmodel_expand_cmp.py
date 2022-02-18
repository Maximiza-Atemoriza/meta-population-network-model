import importlib
import numpy as np
from cmp.compile import compile_model
import matplotlib.pyplot as plt


text = r"""
\frac{dS}{dt} = - \frac{\beta S %I}{%N}\\
\frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I\\
\frac{dR}{dt} = \gamma I
"""

model_name = "SIR_Expand"
compile_model(text, model_name, "./tests/cmodel")
