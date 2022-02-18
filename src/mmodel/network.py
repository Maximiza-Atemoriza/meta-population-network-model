import json
import xml.etree.ElementTree as ET


class Node:
    def __init__(self, idx, label, cmodel):
        self.id = idx
        self.label = label
        self.cmodel = cmodel

    def __str__(self):
        return f"Node(id={self.id}, label={self.label}, model={self.cmodel})"

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __str__(self):
        return f"Edge({self.source} -> {self.target}, weight={self.weight})"

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

        graph = data["graph"]

        for _id, node in graph["nodes"].items():
            self.nodes.append(Node(_id, node["label"], node["metadata"]["cmodel"]))

        for edge in graph["edges"]:
            self.edges.append(
                Edge(edge["source"], edge["target"], edge["metadata"]["weight"])
            )

    def __load_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()

        xmlns = "{http://graphml.graphdrawing.org/xmlns}"
        for graph in root.findall(f"{xmlns}graph"):
            for node in graph.findall(f"{xmlns}node"):
                idx = node.attrib["id"]
                cmodel = "SIR"  # default cmodel
                label = idx  # default label
                for data in node.findall(f"{xmlns}data"):
                    if data.attrib["key"] == "d0":
                        cmodel = data.text
                    if data.attrib["key"] == "d1":
                        label = data.text
                self.nodes.append(Node(idx, label, cmodel))

            for edge in graph.findall(f"{xmlns}edge"):
                source = edge.attrib["source"]
                target = edge.attrib["target"]
                weight = 0  # default weight
                for data in edge.findall(f"{xmlns}data"):
                    if data.attrib["key"] == "d2":
                        try:
                            weight = float(data.text)
                        except ValueError:
                            pass

                self.edges.append(Edge(source, target, weight))
