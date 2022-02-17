"""
Test for the constructor of the Network class
"""

from mmodel.network import Network

print('Testing constructor')
print('-------------------------------')

print('Build network from json file...')
network = Network('./tests/mmodel/test_network_ctr/example_network.json')
print('Nodes: ----------------------------------')
print(network.nodes)
print('---------------------------------------')
print('Edges: -------------------------------------')
print(network.edges)
print('----------------------------------------------\n')

print('Build network from xml file...')
network = Network('./tests/mmodel/test_network_ctr/example_network.xml')
print('Nodes: ----------------------------------')
print(network.nodes)
print('---------------------------------------')
print('Edges: -------------------------------------')
print(network.edges)
print('----------------------------------------------\n')


