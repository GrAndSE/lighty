import operator

from .backend import datastore
from .fields import Field


class Query(object):
    '''Query class
    '''
    __slots__ = ('__add__', '__and__', '__call__', '__init__', '__iter__',
                 '__getslice__', '__len__', '__neg__', '__not__', '__or__',
                 'distinct', 'include', 'exclude', 'fetch', 'from_query',
                 'values', '_cache', 'dist', '_from_query', 'limit', 'model',
                 'operation', 'operand', 'order', 'offset', )

    def __init__(self, operand=None, operation=operator.__and__,
                       from_query=None, offset=0, limit=None, model=None):
        '''Create new query in a form
        from_query operation operand
        '''
        self._cache = None
        self._from_query = from_query
        self.operation = operation
        self.operand = operand
        self.dist = False
        self.order = None
        self.offset = offset
        self.limit = limit
        if from_query is not None:
            self.model = from_query.model
            self.dist = from_query.dist
            self.order = from_query.order
            if from_query.offset > 0:
                self.offset += from_query.offset
            if from_query.limit:
                self.limit = from_query.limit
        elif operand is not None:
            self.model = operand.model
        elif model is not None:
            self.model = model
        else:
            raise AttributeError('Query requires model to be specified')

    def __and__(self, operand):
        '''Creates new query from this query with operation AND and specified
        operand:

            >>> Query(ModelClass.field > 10) & Query(ModelClass.field < 20)
            SELECT * FROM modelclass WHERE field > 10 AND field < 20
        '''
        return Query(operand=operand, operation=operator.__and__,
                     from_query=self)
    __mul__ = __and__
    filter = __and__
    where = __and__

    def __neg__(self):
        '''Get query excludes values

            >>> not Query(ModelClass.field > 0)
            SELECT * FROM modelclass WHERE NOT (field > 0)
        '''
        return Query(operation=operator.__not__, from_query=self)

    def __sub__(self, operand):
        '''Creates new query from this query with operation AND and specified
        operand:

            Query(ModelClass.field > 10) & Query(ModelClass.field < 20)

        equivalent to:

            SELECT * FROM modelclass WHERE field > 10 AND field < 20
        '''
        return Query(operand=Query(operator.__not__, operand),
                     operation=operator.__and__, from_query=self)
    exclude = __sub__

    def __or__(self, operand):
        '''Creates new query from this query with operation OR and specified
        operand
        '''
        return Query(operand=operand, operation=operator.__or__,
                     from_query=self)
    __add__ = __or__
    include = __or__

    def __repr__(self):
        '''Get string representation includes class name and query string

            >>> Query(ModelClass.field > 0)
            <Query: "SELECT * FROM modelclass WHERE field > 0">
        '''
        return '<Query: "%s">' % self.__str__()

    def __str__(self):
        '''Get the query string

            >>> str(Query(ModelClass.field > 0))
            SELECT * FROM modelclass WHERE field > 0
        '''
        if self._from_query is None:
            if self.operation == operator.__not__:
                return '%s (%s)' % (operator.__not__, str(self.operation))
            return str(self.operand)
        return '(%s) %s %s' % (str(self._from_query), self.operation,
                               self.operand)

    def distinct(self):
        '''Return's a query copy with distinct modifier
        '''
        query = Query(operand=self.operand, operation=self.operation,
                      from_query=self._from_query, model=self.model)
        query.dist = True
        return query

    def order_by(self, *args):
        '''Query ordering
        '''
        for field in args:
            if not isinstance(field, Field):
                raise AttributeError('You can sort only by model fields')
            elif field.model != self.model.__name__:
                raise AttributeError("%s.%s not from model %s" % (field.name,
                                     field.model, self.model.__name__))
        query = Query(operand=self.operand, operation=self.operation,
                      from_query=self._from_query, model=self.model)
        query.order = args
        return query

    def __call__(self):
        '''Returns the query that copies current query
        '''
        return Query(operand=self.operand, operation=self.operation,
                     from_query=self._from_query, model=self.model)

    def fetch(self, cache=False):
        '''Fetch the result
        '''
        if cache:
            self._cache = [item for item in self]
        return self.__iter__()

    def values(self, fields):
        '''Return's dictionary of fields for specified model
        '''
        return [item for item in datastore.query(self, fields)]

    def __iter__(self):
        '''Returns and iterator throuch data from datastore
        '''
        if self._cache:
            for item in self._cache:
                yield item
        for item in datastore.query(self):
            yield self.model(is_new=False, **item)

    def __len__(self):
        '''Get number of items in query
        '''
        return len(self._cache) if self._cache else datastore.count(self)

    def __getslice__(self, i=0, j=None):
        '''Get the query that contains a slice of current query
        '''
        return Query(from_query=self._from_query, model=self.model,
                     offset=i, limit=j)
