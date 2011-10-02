AND = '&'
OR  = '|'
NOT = '!'


class Query(object):
    '''Query class
    '''
    __slots__ = ('from_query', 'operation', 'operand', 'model')

    def __init__(self, operation, operand, from_query=None, model=None):
        self.from_query = from_query
        self.operation  = operation
        self.operand    = operand
        if from_query is not None:
            self.model  = from_query.model
        elif model is not None:
            self.model  = model
        else:
            raise AttributeError('Query requires model to be specified')

    def __and__(self, operand):
        return Query(AND, operand, self)
    __mul__ = __and__
    filter  = __and__
    where   = __and__

    def __neg__(self):
        return Query(NOT, None, self)

    def __sub__(self, operand):
        return Query(AND, Query(NOT, operand, None), self)
    exclude = __sub__

    def __or__(self, operand):
        return Query(OR, operand, self)
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
