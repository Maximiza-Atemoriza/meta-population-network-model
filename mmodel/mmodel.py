from .network import Network
import json
from utils.imports import import_from_file
from utils.hashing import hash_file
import importlib

NAME = 'name'
CONFIG_FILE = 'config-file'
NETWORK_FILE = 'network-file'
CODE_FILE = 'code-file'
NETWORK_HASH = 'network-hash'

def load_model(cmodel):
    module = importlib.import_module(f'cmodel.repo.{cmodel}')
    return getattr(module, cmodel)

# Base class for meta models
class MetaModel:
    def __init__(self, *args):
        if len(args) == 1:
            self.__load_model__(args[0])
            self.network = Network(self.net_file)
        elif len(args) == 2:
            self.name = args[0]
            self.net_file = args[1]
            self.net_file_hash = None
            
            self.path = self.net_file[:self.net_file.rfind('/')] # generated files
            self.code_file = f'{self.path}/{self.name}.py' 
            self.config_file = f'{self.path}/{self.name}.cnf.json'

            self.network = Network(self.net_file)
            self.compile()
        else:
            raise Exception('Paremeter exception')

    

    def simulate(self, input_file, t):
        if hash_file(self.net_file) != self.net_file_hash:
            print(f'hash of network file {self.net_file} changed, recompiling...')
            self.network = Network(self.net_file)
            self.compile()
        else:
            print('hash matched')

        try:
            y, params = self.import_input(input_file)  
        except FileNotFoundError:
            print('Input file not exists')
            return None

        model = import_from_file(self.name, self.code_file)
        
        ret = model.solve(y, t, params).T
        
        cmodels = {}
        results = {}
        
        curr = 0 # current result
        for node in self.network.nodes:
            try:
                cmodel = cmodels[node.cmodel]
            except KeyError:
                cmodel = cmodels[node.cmodel] = load_model(node.cmodel)

            results[node.id] = dict(zip(cmodel.sets, ret[curr:curr+len(cmodel.sets)]))
            curr += len(cmodel.sets)

        return results



    def compile(self):
        
        structures = self.__compute_structures__()

        code = self.__generate_code__(structures) 
        
        with open(self.code_file, 'w') as f:
            f.write(code)

        self.net_file_hash = hash_file(self.net_file) 

        self.__save_model__()
    
    def __compute_structures__(self):
        raise NotImplementedError()

    def __generate_code__(self, structures):    
        raise NotImplementedError()

    def export_input(self, file):
        network = self.network
        inputd = []
        cmodels = {}
        for node in network.nodes:
            try:
                cmodel = cmodels[node.cmodel]
            except KeyError:
                cmodel = cmodels[node.cmodel] = load_model(node.cmodel)

            y =  dict(zip(cmodel.sets, iter(lambda:0, 1)))

            params = dict(zip(cmodel.params, iter(lambda:0, 1)))

            node_input = {
                'id' : node.id,
                'label' : node.label,
                'model' : node.cmodel,
                'y' : y,
                'params' : params
            }

            inputd.append(node_input)

        with open(file, 'w') as f:
            json.dump(inputd, f)

    def import_input(self, file):
        inputd = None
        with open(file, 'r') as f:
            inputd = json.load(f)

        y = []
        params = []

        for node in inputd:
            y += list(node['y'].values())
            params += list(node['params'].values())

        return y, params

    def __save_model__(self):
        config = {
            NAME : self.name,
            CONFIG_FILE : self.config_file,
            NETWORK_FILE : self.net_file,
            CODE_FILE : self.code_file,
            NETWORK_HASH : self.net_file_hash
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def __load_model__(self, config_file):
        config = None
        
        with open(config_file, 'r') as f:
            config = json.load(f)

        self.name = config[NAME]
        self.config_file = config[CONFIG_FILE]
        self.net_file = config[NETWORK_FILE]
        self.code_file = config[CODE_FILE]
        self.net_file_hash = config[NETWORK_HASH]

