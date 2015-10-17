from pkgutil import walk_packages
from importlib import import_module
import inspect


def get_functions(package_path, package_name):
    result = {}
    for _loader, module_name, ispkg in walk_packages(package_path, prefix=package_name + "."):
        module = import_module(module_name)

        def _function_predicate(value):
            return (inspect.isfunction(value) and
                    not value.__name__[0] == "_" and
                    value.__module__.startswith(module_name))

        for function_name, function in inspect.getmembers(module, predicate=_function_predicate):
            if function_name in result:
                raise NameError("The name %s has been defined in both %s and %s." %
                                (function_name, module_name, result[function_name].__module__))
            result[function_name] = function
    return result
