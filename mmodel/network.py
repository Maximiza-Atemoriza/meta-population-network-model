class Node:
    def __init__(self, idx, label, cmodel):
        self.id = idx
        self.label = label
        self.cmodel = cmodel

class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight


class Network:
    def __init__(self, file):
        self.load(file)
    
    def load(self, file):
        self.nodes = [
            Node(1, '1', 'SIR'),
            Node(2, '2', 'SIR')
        ]
        self.edges = [
            Edge(1, 2, 0.8),
            Edge(2, 1, 0.1)
        ]

    
    def save(self, file):
        raise NotImplementedError()
    
    def __load_json(self, file):
        raise NotImplementedError()
    
    def __save_json(self, file):
        raise NotImplementedError()


