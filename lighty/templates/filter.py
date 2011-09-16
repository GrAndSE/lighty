"""Package provides template filters management
"""

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

    def apply(self, filter, value, args, context):
        '''Apply filter to values
        '''
        filter_func = self.is_filter_exists(filter)
        return filter_func(value, *args)


filter_manager = FilterManager()
