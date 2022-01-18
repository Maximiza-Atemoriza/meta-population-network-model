import inspect
import importlib
import os
import sys


class CModels:
    def __init__(self) -> None:
        pass

    def get(self, name: str):
        # change cwd to import modules 
        sys.path.insert(0, '')
        old_wd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

        module = importlib.import_module(f'repo.{name}')
        _ , class_object = inspect.getmembers(module,lambda x: inspect.isclass(x))[0]

        os.chdir(old_wd)
        return class_object()

