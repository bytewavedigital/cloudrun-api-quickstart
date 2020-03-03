from cerberus import Validator


def validate(data, schema):
    v = Validator(schema)
    return v.validate(data), v.errors
