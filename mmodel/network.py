import json
import xml.etree.ElementTree as ET


class Node:
    def __init__(self, idx, label, cmodel):
        self.id = idx
        self.label = label
        self.cmodel = cmodel
        self.y = None
        self.params = None

    def __str__(self):
        return self.id + "->" + self.label + "_" + self.cmodel + "_" + str(self.y) + "_" + str(self.params)


class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __str__(self):
        return self.source + "->" + self.target + "_" + str(self.weight)


class Network:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def load_nodes(self, file):
        if file.endswith(".json"):
            self.__load_nodes_json(file)
        elif file.endswith(".xml"):
            self.__load_nodes_xml(file)

    def __load_nodes_json(self, file):
        f = open(file)
        data = json.load(f)
        for item in data:
            self.nodes[item["id"]] = (Node(
                item["id"],
                item["label"],
                item["cmodel"]
            ))
            for edge in item["targets"]:
                self.edges.append(Edge(item["id"], edge["target"], edge["weight"]))

    def __load_nodes_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        for node in root:
            for item in node:
                if item.tag == "targets":
                    targets = item

            self.nodes[node.attrib["id"]] = Node(
                node.attrib["id"],
                node.attrib["label"],
                node.attrib["cmodel"]
            )

            for target in targets:
                self.edges.append(Edge(
                    node.attrib["id"],
                    target.attrib["id"],
                    float(target.attrib["weight"]))
                    )

    def load_params(self, file):
        if file.endswith(".json"):
            self.__load_params_json(file)
        elif file.endswith(".xml"):
            self.__load_params_xml(file)

    def __load_params_json(self, file):
        f = open(file)
        data = json.load(f)
        for item in data:
            self.nodes[item["id"]].y = item["y"]
            self.nodes[item["id"]].params = item["params"]

    def __load_params_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        for node in root:
            for item in node:
                if item.tag == "y":
                    y = item.attrib
                    for key, value in y.items():
                        y[key] = float(value)
                elif item.tag == "params":
                    params = item.attrib
                    for key, value in params.items():
                        params[key] = float(value)

            self.nodes[node.attrib["id"]].y = y
            self.nodes[node.attrib["id"]].params = params


net = Network()
net.load_nodes("example_nodes.xml")
net.load_params("example_params.xml")
for _, node in net.nodes.items():
    print(node)
for edge in net.edges:
    print(edge)

print("---------------")

net = Network()
net.load_nodes("example_nodes.json")
net.load_params("example_params.json")
for _, node in net.nodes.items():
    print(node)
for edge in net.edges:
    print(edge)
