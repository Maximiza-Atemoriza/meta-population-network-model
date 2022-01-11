class Node:
    def __init__(self, idx, label, cmodel, y, params):
        self.id = idx
        self.label = label
        self.cmodel = cmodel
        self.y = y
        self.params = params


class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight


class Network:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    
    def load(self, file):
        raise NotImplementedError()
    
    def save(self, file):
        raise NotImplementedError()
    
    def __load_json(self, file):
        raise NotImplementedError()
    
    def __save_json(self, file):
        raise NotImplementedError()


