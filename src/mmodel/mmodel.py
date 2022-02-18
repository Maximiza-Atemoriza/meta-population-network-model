from .network import Network
import json
from utils.imports import import_from_file
from utils.hashing import hash_file
import importlib
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Meta Model input constants
NAME = "name"
CONFIG_FILE = "config-file"
NETWORK_FILE = "network-file"
CODE_FILE = "code-file"
NETWORK_HASH = "network-hash"

# Input file constants
NID = "id"
NLABEL = "label"
NMODEL = "model"
NY = "y"
NPARAMS = "params"


def load_model(cmodel):  # TODO: Replace this with the repository implementation
    module = importlib.import_module(f"cmodel.repo.{cmodel}")
    return getattr(module, cmodel)


# Base abstract class for meta models
class MetaModel:
    def __init__(self, *args):
        if len(args) == 1:
            self.__load_model__(args[0])
            self.network = Network(self.net_file)
        elif len(args) == 2:
            self.name = args[0]
            self.net_file = args[1]
            self.net_file_hash = None

            self.path = self.net_file[: self.net_file.rfind("/")]  # generated files
            self.code_file = f"{self.path}/{self.name}.py"
            self.config_file = f"{self.path}/{self.name}.cnf.json"

            self.network = Network(self.net_file)
            self.compile()
        else:
            raise Exception("Paremeter exception")

    def simulate(self, input_file, t):
        if hash_file(self.net_file) != self.net_file_hash:
            print(f"hash of network file {self.net_file} changed, recompiling...")
            self.network = Network(self.net_file)
            self.compile()
        else:
            print("hash matched")

        try:
            y, params = self.import_input(input_file)
        except FileNotFoundError:
            print("input file not exists")
            return None

        model = import_from_file(self.name, self.code_file)

        ret = model.solve(y, t, params).T

        cmodels = {}
        results = {}

        curr = 0  # current result
        for node in self.network.nodes:
            try:
                cmodel = cmodels[node.cmodel]
            except KeyError:
                cmodel = cmodels[node.cmodel] = load_model(node.cmodel)

            results[node.id] = dict(
                zip(cmodel.sets, ret[curr : curr + len(cmodel.sets)])
            )
            curr += len(cmodel.sets)

        return results

    # ------------------------------------------------------------------
    # This sections conatins the methods that generate the code for
    # the meta model given by the Netork object of the meta model
    # The private methods are intended to be override on implementation
    # classes of specific meta models variations.
    # ------------------------------------------------------------------

    def compile(self):

        structures = self.__compute_structures__()

        code = self.__generate_code__(structures)

        with open(self.code_file, "w") as f:
            f.write(code)

        self.net_file_hash = hash_file(self.net_file)

        self.__save_model__()

    def __compute_structures__(self):
        raise NotImplementedError()

    def __generate_code__(self, structures):
        raise NotImplementedError()

    # ------------------------------------------------------------------
    # This section contains methods to create files that can be
    # used by the users of the the module to introduce the
    # initial conditions and parameters of the nodes in the network
    # for the meta model simulation. This files can be produced by hand
    # so this methods are just for ease of use purposes
    # ------------------------------------------------------------------

    def export_input(self, file):
        network = self.network
        nodes = []

        cmodels = {}
        for node in network.nodes:
            try:
                cmodel = cmodels[node.cmodel]
            except KeyError:
                cmodel = cmodels[node.cmodel] = load_model(node.cmodel)

            y = dict(zip(cmodel.sets, iter(lambda: 0, 1)))
            params = dict(zip(cmodel.params, iter(lambda: 0, 1)))

            nodes.append(
                {
                    NID: node.id,
                    NLABEL: node.label,
                    NMODEL: node.cmodel,
                    NY: y,
                    NPARAMS: params,
                }
            )

        if file.endswith(".json"):
            self.__export_input_json__(nodes, file)
        elif file.endswith(".xml"):
            self.__export_input_xml__(nodes, file)

    def __export_input_json__(self, nodes, file):
        with open(file, "w") as f:
            json.dump(nodes, f)

    def __export_input_xml__(self, nodes, file):
        root = minidom.Document()

        xml = root.createElement("nodes")

        for node in nodes:
            tree_node = root.createElement(node[NLABEL])

            tree_node.setAttribute(NID, node[NID])
            tree_node.setAttribute(NLABEL, node[NLABEL])
            tree_node.setAttribute(NMODEL, node[NMODEL])

            ny = root.createElement(NY)
            nparams = root.createElement(NPARAMS)

            for key, value in node[NY].items():
                ny.setAttribute(key, value)

            for key, value in node[NPARAMS].items():
                nparams.setAttribute(key, value)

            ytext = root.createTextNode(
                "Puede modificar los atributos de este elemento"
            )
            ny.appendChild(ytext)
            paramstext = root.createTextNode(
                "Puede modificar los atributos de este elemento"
            )
            nparams.appendChild(paramstext)

            tree_node.appendChild(ny)
            tree_node.appendChild(nparams)

            xml.appendChild(tree_node)

        xml_str = xml.toprettyxml(indent="\t")

        with open(file, "w") as f:
            f.write(xml_str)

    # ---------------------------------------------------------
    # This section contains methods for importing the initial
    # conditions and parameters of the nodes in the network
    # for the meta model simulation
    # ---------------------------------------------------------

    def import_input(self, file):
        if file.endswith(".json"):
            return self.__import_input_json__(file)
        elif file.endswith(".xml"):
            return self.__import_input_xml__(file)

    def __import_input_json__(self, file):
        nodes = None
        with open(file, "r") as f:
            nodes = json.load(f)

        y = []
        params = []

        for node in sorted(nodes, key=lambda x: x[NID]):
            y += list(node[NY].values())
            params += list(node[NPARAMS].values())

        return y, params

    def __import_input_xml__(self, file):
        nodes = []
        tree = ET.parse(file)
        root = tree.getroot()
        for node in root:
            for item in node:
                if item.tag == NY:
                    nodey = {key: float(value) for key, value in item.attrib.items()}
                elif item.tag == NPARAMS:
                    nodeparams = {
                        key: float(value) for key, value in item.attrib.items()
                    }
            nodes.append((int(node.attrib[NID]), nodey, nodeparams))

        y = []
        params = []
        for node in sorted(nodes, key=lambda x: x[0]):
            y += list(node[1].values())
            params += list(node[2].values())

        return y, params

    # ----------------------------------------------------------
    # This section contains methods for loading and saving the
    # configuration of the current Meta Model instance
    # ----------------------------------------------------------

    def __save_model__(self):
        config = {
            NAME: self.name,
            CONFIG_FILE: self.config_file,
            NETWORK_FILE: self.net_file,
            CODE_FILE: self.code_file,
            NETWORK_HASH: self.net_file_hash,
        }

        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def __load_model__(self, config_file):
        config = None

        with open(config_file, "r") as f:
            config = json.load(f)

        self.name = config[NAME]
        self.config_file = config[CONFIG_FILE]
        self.net_file = config[NETWORK_FILE]
        self.code_file = config[CODE_FILE]
        self.net_file_hash = config[NETWORK_HASH]
