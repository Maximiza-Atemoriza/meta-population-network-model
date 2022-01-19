from mmodel.flux import FluxMetaModel

net_file = './tests/mmodel/test_input_export/example_network.json'
name = 'example_network'

model = FluxMetaModel(name, net_file)

model.export_input('./tests/mmodel/test_input_export/input_files/input.json')
print('Exported input in json format')
model.export_input('./tests/mmodel/test_input_export/input_files/input.xml')
print('Exported input in xml format')
