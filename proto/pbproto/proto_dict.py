import sys
import os.path

_PROTO_DICT = {}

def load_dir(topdir):
    def visit(arg, dirname, names):
        for i in names:
            filepath = os.path.join(dirname, i)
            if os.path.isfile(filepath) and filepath.endswith('.py'):
                try:
                    load_file(filepath[len(topdir) + 1:])
                except AttributeError:
                    pass
    os.path.walk(topdir, visit, None)

def load_message(desc, cls):
    descs = desc.nested_types_by_name
    for k in descs:
        desc = descs[k]
        if hasattr(cls, k):
            nested_cls = getattr(cls, k)
            _PROTO_DICT[desc.full_name] = nested_cls
            load_message(desc, nested_cls)

def load_file(filename):
    root, ext = os.path.splitext(filename)
    module_name = root.replace(os.path.sep, '.')
    module = __import__(module_name, fromlist=module_name.split('.'), level=0)
    descs = module.DESCRIPTOR.message_types_by_name
    for k in descs:
        desc = descs[k] 
        if hasattr(module, k):
            cls = getattr(module, k)
            _PROTO_DICT[desc.full_name] = cls 
            load_message(desc, cls)

def get(key):
    if key:
        return _PROTO_DICT[key]
    return None
