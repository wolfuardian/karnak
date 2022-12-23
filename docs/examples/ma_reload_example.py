def reload_all():
    print('On exec reload_all function ...')
    import python.eil.util.common
    try:
        reload(python.eil.util.common)
        print('Module python.eil.util.common has reloaded!')

    except AttributeError:
        pass

    import python.eil.util.qt
    try:
        reload(python.eil.util.qt)
        print('Module python.eil.util.qt has reloaded!')

    except AttributeError:
        pass


reload_all()
