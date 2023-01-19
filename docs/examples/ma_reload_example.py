def reload_all():
    print('On exec reload_all function ...')

    # python.eil.util.common
    import python.eil.util.common
    try:
        reload(python.eil.util.common)
        print('Module python.eil.util.common has reloaded!')

    except AttributeError:
        pass

    # python.eil.util.qt
    import python.eil.util.qt
    try:
        reload(python.eil.util.qt)
        print('Module python.eil.util.qt has reloaded!')

    except AttributeError:
        pass

    # python.eil.mixin.menu
    import python.eil.mixin.menu
    try:
        reload(python.eil.mixin.menu)
        print('Module python.eil.mixin.menu has reloaded!')

    except AttributeError:
        pass


reload_all()
