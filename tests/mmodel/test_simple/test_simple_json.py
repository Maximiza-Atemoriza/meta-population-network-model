from mmodel.flux import FluxMetaModel
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 160, 160)
# Test constructor

net_file = "./tests/mmodel/test_flux/example_network.json"
name = "example_network"

mmodel = FluxMetaModel(name, net_file)
