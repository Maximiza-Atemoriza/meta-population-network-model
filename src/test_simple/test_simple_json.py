from mmodel.simple_trip import SimpleTripMetaModel
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 160, 160)
# Test constructor

net_file = "./src/test_simple/example_network.json"
name = "example_network"

mmodel = SimpleTripMetaModel(name, net_file)
