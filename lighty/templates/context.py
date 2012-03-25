'''Methods for context accessing
'''
from functools import reduce


def get_value(var_name, context):
    return context[var_name] if var_name in context else None


def get_field(obj, field):
    if hasattr(obj, field):
        return getattr(obj, field)
    elif hasattr(obj, '__getitem__') and hasattr(obj, '__contains__'):
        return obj[field]
    raise Exception('Could not get %s from %s' % (field, obj))


def resolve(var_name, context):
    if '.' in var_name:
        fields = var_name.split('.')
        return reduce(get_field, [get_value(fields[0], context)] + fields[1:])
    return get_value(var_name, context)
