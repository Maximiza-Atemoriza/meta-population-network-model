import json
import xml.etree.ElementTree as ET


class Node:
    def __init__(self, idx, label, cmodel):
        self.id = idx
        self.label = label
        self.cmodel = cmodel

    def __str__(self):
        return f'Node(id={self.id}, label={self.label}, model={self.cmodel})'
    
    def __repr__(self):
        return self.__str__()

class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __str__(self):
        return f'Edge({self.source} -> {self.target}, weight={self.weight})'
    
    def __repr__(self):
        return self.__str__()

class Network:

    def __init__(self, file):
        self.nodes = []
        self.edges = []
        self.load(file)
        

    def load(self, file):
        if file.endswith(".json"):
            self.__load_json(file)
        elif file.endswith(".xml"):
            self.__load_xml(file)

    def __load_json(self, file):
        f = open(file)
        data = json.load(f)
        for item in data:
            self.nodes.append(Node(
                item["id"],
                item["label"],
                item["cmodel"]
            ))
            for edge in item["targets"]:
                self.edges.append(Edge(item["id"], edge["target"], edge["weight"]))

    def __load_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        for node in root:
            for item in node:
                if item.tag == "targets":
                    targets = item

            self.nodes.append(Node(
                node.attrib["id"],
                node.attrib["label"],
                node.attrib["cmodel"]
            ))

            for target in targets:
                self.edges.append(Edge(
                    node.attrib["id"],
                    target.attrib["id"],
                    float(target.attrib["weight"]))
                    )

