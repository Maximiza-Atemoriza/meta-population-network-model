# This file provides an interface to handle CRUD operations for models
import json
from metapopulation_network_model.compile import compile_model
import os

class ModelRepository:
    models = None # dictionary to store the models in memory
    path = None # path to the models repository
    
    @staticmethod
    def start(repository_path):
        ModelRepository.path = repository_path
        with open(f'{ModelRepository.path}/models.json', 'r') as f:
            ModelRepository.models = json.load(f)
        print(f'Started model repository service at {ModelRepository.path}')

    @staticmethod
    def exists_model(name):
        try:
            ModelRepository.models[name]
            return True
        except KeyError:
            return False

    @staticmethod
    def get_model_names():
        return ModelRepository.models.keys()

    @staticmethod
    def get_model(name):
        try:
            return ModelRepository.models[name]
        except KeyError:
            return None

    @staticmethod
    def add_model(name, description, features, equations):
        if ModelRepository.exists_model(name):
            raise Exception("There is already a model with the same name")
        compile_model(equations, name, 'models')
        ModelRepository.models[name] = {
                'description' : description,
                'features': features,
                'equations': equations,
                'code': f'{ModelRepository.path}/{name}.py'
                }

        with open(f'{ModelRepository.path}/models.json', 'w') as f:
            json.dump(ModelRepository.models, f)
    
    @staticmethod
    def remove_model(name):
        os.remove(ModelRepository.models[name]['code'])
        del ModelRepository.models[name]
        with open(f'{ModelRepository.path}/models.json', 'w') as f:
            json.dump(ModelRepository.models, f)
