# Meta-population network models


## Goals

- Use different compartmental models in the nodes of the network.
- Use different movement models in the edges of the network.
- Graphic the pandemic behaviour in a selected node of the network.
- Graphic the pandemic behaviour in the hole network.

## Design Considerations

This section will contain discussion points about the design of the application.

## Assumptions

Assumptions of the project

## Notation and glossary

- `cmodel` : stands for compartmental model
- `mmodel`: stands for meta-population model

## Modules
---
### CModel
This model functionalities include: compiling a compartmental model from LaTex code to python code and must include a repository to retrieve, update and delete the models.

#### Compiling
Your comments here

#### Repository
Your comments here

---
### MModel
The functionality of this module is to receive a `Network` and compute the results of the given model.

#### Network

This module is based in an OOP oriented design and implements network functionalities in the application.

A `Node` is defined as `Node(id: int, label: string, cmodel: cid, y0: float[], params: float[])` where `y0` and `params` are the initial conditions and parameters respectively of the compartmental model `cmodel`.

An `Edge` can be defined as `Edge(source_node: int, target_node: int, weight: float)`

A `Network` is considered to be a structure with a set of `nodes` and a set of `edges`, so it can be defined as `Network(nodes: Node[], edges: Edge[])`.

Since the networks used in this application can be quite large it becomes necessary an encoding method to load and save networks for ease of use for both final user and developers. With the goal in mind of not base other modules logic in the file format chosen to encode the networks the class `network` defines  methods `load(file)` and `save(file)` that detect the extension of the file format from the parameter `file` and then call the format specific encoding method. For example:

```python
class network:
	#... some definitions ...
	
	# this will be the interface for all encoding methods
	def load(file):
		if file.extension == 'json':
			load_json(file)
		# ...
		
	def save(file):
		if file.extension == 'json':
			save_json(file)
		# ...
		
	# actual encoding methods
	def load_json(file):
		pass
	
	def save_json(file):
		pass
```
---
### UI
Your comments here





