import os
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec

def load_module(name, path):
    # Import external modules programmatically with importlib.
    loader = SourceFileLoader(name, path)
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module

def load_modules(dir):
    # Crawl through directories searching for Python modules,
    # and return an object containing each of them.
    modules = {}
    list_dir = os.listdir(dir)
    for name in list_dir:

        path = f'{dir}/{name}'

        # Ignore `__init__.py` special case.
        if name == "__init__.py":
            continue

        # File or directory?
        if os.path.isdir(path):
            # Load directories recursively.
            new_modules = load_modules(path)
            modules.update(new_modules)
            
        else:
            # Load the file at the given path.
            path = f'{dir}/{name}'
            module = load_module(name, path)

            # Check whether a function by the same name is in the Python script.
            func_name = name_split = name.split('.')[0]
            if hasattr(module, func_name):
                # If found, add to modules object.
                modules[func_name] = getattr(module, func_name)
            else:
                # Otherwise log the error and require a keypress to draw attention to it.
                print(f'<!> File name does not match name of function in "{name}"! Skipping.')
                input("Press any key to continue.")
                continue

    return modules