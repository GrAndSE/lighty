'''Some utilitary classes usually used to make working with different python
versions and different environment easier:

- string_types - basestring for python 2 and str fot python 3
- dict_keys - convert dict keys to list
- div_operators - operators for division
- with_metaclass - metaclasses
'''
import sys
import operator

PY3 = sys.version_info[0] == 3
div_operators = (operator.__truediv__, operator.__floordiv__)
if PY3:
    string_types = str
    dict_keys = lambda keys: [i for i in keys.__iter__()]
else:
    string_types = basestring
    dict_keys = lambda keys: keys
    div_operators += (operator.__div__, )


def with_metaclass(meta, base=object):
    '''Create a new class with base class base and metaclass metaclass. This is
    designed to be used in class declarations like this::

        from lighty.utils import with_metaclass

        class Meta(type):
            pass

        class Base(object):
            pass

        class MyClass(with_metaclass(Meta, Base)):
            pass
    '''
    return meta("NewBase", (base, ), {})
