from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec

def load_module(name, path):
    # Import external modules programmatically with importlib.
    loader = SourceFileLoader(name, path)
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module