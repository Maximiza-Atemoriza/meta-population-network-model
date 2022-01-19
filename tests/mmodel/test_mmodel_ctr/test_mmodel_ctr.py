"""
Test the constructor of a meta model and its compilation process
"""

from mmodel.flux import FluxMetaModel

net_file = './tests/mmodel/test_mmodel_ctr/example_network.json'
name = 'example_network'
model = FluxMetaModel(name, net_file)

model = FluxMetaModel(f'./tests/mmodel/test_mmodel_ctr/{name}.cnf.json')

net = model.network

print('Nodes: -------------------------------------')
print(net.nodes)
print('Edges: ---------------------------------------')
print(net.edges)

# This should output the network of the example
