import glob
import os


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
        __file_string += __pattern
        __file_all_group.append(glob.glob(os.path.join(path, '{0}.{1}'.format(__file_string, file_ext))))

    for file_group in __file_all_group:
        for file in [file for file in file_group if (basename(file) not in basenames(__file_all))]:
            __file_all.append(file)

    return __file_all


def reload_all_mod():
    import eil.util.common
    import eil.util.qt
    reload(eil.util.common)
    reload(eil.util.qt)
