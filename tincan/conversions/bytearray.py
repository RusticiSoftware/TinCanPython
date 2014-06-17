def make_bytearray(value):
    if isinstance(value, unicode):
        return bytearray(value, 'utf-8')
    else:
        return bytearray(value)


def jsonify_bytearray(value):
    return value.decode('utf-8')