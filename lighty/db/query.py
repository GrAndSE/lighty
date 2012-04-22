from backend import datastore
from fields import Field
from operations import AND, NOT, OR


class Query(object):
    '''Query class
    '''
    __slots__ = ('from_query', 'operation', 'operand', 'model', 'dist',
                 'order', 'offset', 'limit', )

    def __init__(self, operand=None, operation=AND,
                       from_query=None, model=None):
        '''Create new query in a form
        from_query operation operand
        '''
        self.from_query = from_query
        self.operation = operation
        self.operand = operand
        self.dist = False
        self.order = None
        self.offset = 0
        self.limit = None
        if from_query is not None:
            self.model = from_query.model
            self.dist = from_query.dist
            self.order = from_query.order
            self.offset = from_query.offset
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
        return Query(operand=operand, operation=AND, from_query=self)
    __mul__ = __and__
    filter = __and__
    where = __and__

    def __neg__(self):
        return Query(operation=NOT, from_query=self)

    def __sub__(self, operand):
        '''Creates new query from this query with operation AND and specified
        operand:

            Query(ModelClass.field > 10) & Query(ModelClass.field < 20)

        equivalent to:

            SELECT * FROM modelclass WHERE field > 10 AND field < 20
        '''
        return Query(operand=Query(NOT, operand), operation=AND,
                     from_query=self)
    exclude = __sub__

    def __or__(self, operand):
        '''Creates new query from this query with operation OR and specified
        operand
        '''
        return Query(operand=operand, operation=OR, from_query=self)
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
        if self.from_query is None:
            if self.operation == NOT:
                return '%s (%s)' % (NOT, str(self.operation))
            return str(self.operand)
        return '(%s) %s %s' % (str(self.from_query), self.operation,
                               self.operand)

    def distinct(self):
        '''Return's a query copy with distinct modifier
        '''
        query = Query(operand=self.operand, operation=self.operation,
                      from_query=self.from_query, model=self.model)
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
                      from_query=self.from_query, model=self.model)
        query.order = args
        return query

    def __call__(self):
        '''Returns the query that copies current query
        '''
        return Query(operand=self.operand, operation=self.operation,
                     from_query=self.from_query, model=self.model)

    def fetch(self):
        '''Fetch the result
        '''
        return self.__iter__()

    def values(self, fields):
        '''Return's dictionary of fields for specified model
        '''
        return datastore.query(self, fields)

    def __iter__(self):
        '''Returns and iterator throuch data from datastore
        '''
        for item in datastore.query(self):
            yield self.model(is_new=False, **item)

    def __getslice__(self, i, j):
        '''Get slice
        '''
        return datastore.slice(self, i, j)
