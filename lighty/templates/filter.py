"""Package provides template filters management
"""
import string
from .context import resolve


class FilterManager(object):
    """Class used for filters manipulations
    """
    __slots__ = ('apply', 'filters', 'is_filter_exists', )

    def __init__(self):
        """Create new tag managet instance
        """
        super(FilterManager, self).__init__()
        self.filters = {}

    def is_filter_exists(self, name):
        """Check is filter exists
        """
        if name not in self.filters:
            raise Exception("Filter '%s' is not registered" % name)
        return self.filters[name]

    def register(self, filter):
        '''Register filter in manager
        '''
        self.filters[filter.__name__] = filter

    def apply(self, filter, value, args, arg_types, context):
        '''Apply filter to values
        '''
        filter_func = self.is_filter_exists(filter)
        new_args = []
        i = 0
        while i < len(args):
            new_args.append(arg_types[i] and args[i] or context[args[i]])
            i += 1
        return filter_func(value, *new_args)

filter_manager = FilterManager()
