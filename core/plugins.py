def register(plugin):
    a = {}
    for key, value in plugin.items():
        if callable(value):
            a[key] = value()
        else:
            a[key] = value
    return a
