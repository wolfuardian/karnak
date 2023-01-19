import glob
import os


def rebind_dict(keys, values):
    return dict(map(lambda i, j: (i, j), keys, values))


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class ConstantDict(AttributeDict):
    def __setattr__(self, key, value):
        if key in self:
            raise RuntimeError("Can't rebind const (%s)" % key)
        else:
            super(ConstantDict, self).__setattr__(key, value)


class _Listener(object):
    """
    Process registration class
    """

    def __init__(self, container):
        self.__container = container

    def add(self, func):
        self.__container.append(func)

    def remove(self, func):
        if func in self.__container:
            self.__container.remove(func)


class Subject(object):
    """
    Processing notification class
    """

    def __init__(self):
        self.__functions = []
        self.__listener = _Listener(self.__functions)

    def emit(self, *args, **kwargs):
        for func in self.__functions:
            func(*args, **kwargs)

    @property
    def listen(self):
        # type: () -> _Listener
        return self.__listener


def get_attr_chain(obj, attr_chain):
    """
    Dot-delimited Attribute from object
    """
    attrs = attr_chain.split('.')
    if hasattr(obj, attrs[0]):
        if len(attrs) == 1:
            return getattr(obj, attrs[0])
        else:
            return get_attr_chain(getattr(obj, attrs[0]), '.'.join(attrs[1:]))
    else:
        return None


def basename(path):
    return os.path.basename(path)


def basenames(paths):
    __file_all = []
    for path in paths:
        __file_all.append(basename(path))

    return __file_all


def list_files(path, file_ext, __depth=5):
    __file_all = []
    __file_all_group = []
    __file_string = '*'
    __pattern = '/*'
    __depth = 5
    for i in range(__depth):
        __file_all_group.append(glob.glob(os.path.join(path, '{0}.{1}'.format(__file_string, file_ext))))
        __file_string += __pattern

    for file_group in __file_all_group:
        for file in [file for file in file_group if (basename(file) not in basenames(__file_all))]:
            file = file.replace('\\', '/')
            __file_all.append(file)

    return __file_all


def reload_all_mod():
    import eil.util.common
    import eil.util.qt
    reload(eil.util.common)
    reload(eil.util.qt)
