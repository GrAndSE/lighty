from backend import datastore
from fields import Field
from operations import AND, NOT, OR


class Query(object):
    '''Query class
    '''
    __slots__ = ('from_query', 'operation', 'operand', 'model', 'dist', 'order')

    def __init__(self, operand=None, operation=AND, 
                       from_query=None, model=None):
        '''Create new query in a form
        from_query operation operand
        '''
        self.from_query = from_query
        self.operation  = operation
        self.operand    = operand
        self.dist       = False
        self.order      = None
        if from_query is not None:
            self.model  = from_query.model
            self.dist   = from_query.dist
            self.order  = from_query.order
        elif operand is not None:
            self.model  = operand.model
        elif model is not None:
            self.model  = model
        else:
            raise AttributeError('Query requires model to be specified')

    def __and__(self, operand):
        '''Creates new query from this query with operation AND and specified
        operand
        '''
        return Query(operand=operand, operation=AND, from_query=self)
    __mul__ = __and__
    filter  = __and__
    where   = __and__

    def __neg__(self):
        return Query(operation=NOT, from_query=self)

    def __sub__(self, operand):
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
        return '<Query: %s>' % self.__str__()

    def __str__(self):
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
        '''Returns the query copy
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
        return datastore.slice(self, i, j)
