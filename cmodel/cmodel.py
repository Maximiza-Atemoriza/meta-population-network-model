import inspect
import importlib

class CModels:
    def __init__(self) -> None:
        pass

    def get(self, name: str):
        module = importlib.import_module(f'repo.{name}')
        _ , class_object = inspect.getmembers(module,lambda x: inspect.isclass(x))[0]
        return class_object()

