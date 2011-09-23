'''Package contains default template tags
'''
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from operator import itemgetter
import random as random_module

from filter import filter_manager


# Numbers

def sum(*args):
    '''Calculate the sum of all the values passed as args and
    '''
    return reduce(lambda x, y: x + float(y), args)
filter_manager.register(sum)

def float_format_args_parse(func, raw_value, format):
    # Parse arguments
    try:
        digits  = abs(int(format))
    except:
        raise Exception('%s arguments error: format is not integer' % func)
    try:
        value   = Decimal(raw_value)
    except:
        raise Exception('%s supports only number values' % func)
    return value, digits

def do_float_format(value, digits, rounding):
    # Make formater
    digit = 0
    formatter = Decimal('1')
    while digit < digits:
        digit += 1
        formatter *= Decimal('0.1')
    return value.quantize(formatter, rounding=rounding)

def floatformat(raw_value, format='0'):
    '''Make pretty float representation

    Lets:
        a = '12.4'
    Then:
        >>> print floatformat(a)
        12
        >>> print floatformat(a, '2')
        12.40
        >>> print floatformat(a, '-2')
        12.4
    '''
    value, digits = float_format_args_parse('floatformat', raw_value, format)
    result = do_float_format(value.copy_abs(), digits, ROUND_DOWN)
    result = str(result.copy_sign(value))
    if format[0] == '-':
        return result.rstrip('0')
    return result
filter_manager.register(floatformat)

def floatround(raw_value, format="0"):
    '''Round a float value according to math rules

    Lets:
        a = '12.45'
    Then:
        >>> print floatround(a)
        12
        >>> print floatround(a, '1')
        12.5
    '''
    value, digits = float_format_args_parse('floatround', raw_value, format)
    return do_float_format(value, digits, ROUND_HALF_UP)
filter_manager.register(floatround)


# Strings

def addslashes(value):
    '''Add a slashes to string
    '''
    return value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
filter_manager.register(addslashes)

def capfirst(value):
    '''Capitalizes the first character in string
    '''
    return value and value[0].upper() + value[1:]
filter_manager.register(capfirst)

def stringformat(value, format):
    """Formats the variable according to the format, a string formatting 
    specifier.
        
    This specifier uses Python string formating syntax, with the exception that
    the leading "%" is dropped.

    See http://docs.python.org/lib/typesseq-strings.html for documentation
    of Python string formatting
    """
    return (u"%" + str(format)) % value
filter_manager.register(stringformat)

def upper(value):
    '''Convert to upper case
    '''
    return str(value).upper()

def lower(value):
    '''Convert to lower case
    '''
    return str(value).lower()


# Lists, dicts, strings

def dictsort(value, key, order=''):
    '''Sort dict
    '''
    return sorted(value, key=itemgetter(key), reverse=(order != ''))
filter_manager.register(dictsort)

def get(value, index):
    '''Get item with specified index
    '''
    if issubclass(value.__class__, dict):
        return value[sorted(value.keys())[index]]
    return value[index]
filter_manager.register(get)

def first(value):
    '''Get first item from list
    '''
    return get(value, 0)
filter_manager.register(first)

def join(value, joiner):
    '''Join list or items with joiner

    >>> join([1, 2, 3], ' ')
    '1 2 3'
    '''
    return joiner.join([str(item) for item in value])
filter_manager.register(join)

def last(value):
    '''Get last item from list
    '''
    return get(value, len(value) - 1)
filter_manager.register(last)

def length(value):
    '''Return's the length of the string, dict or list
    '''
    return len(value)

def random(value):
    '''Get random item from list or dict
    '''
    return get(value, random_module.random(len(value)))
filter_manager.register(random)

def sort(value, order=''):
    '''Sort list
    '''
    return sorted(value, reverse=(order != ''))
filter_manager.register(sort)
