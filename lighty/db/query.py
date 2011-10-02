AND = '&'
OR  = '|'
NOT = '!'


class Query(object):
    '''Query class
    '''
    __slots__ = ('from_query', 'operation', 'operand', 'model')

    def __init__(self, operand=None, operation=AND, 
                       from_query=None, model=None):
        self.from_query = from_query
        self.operation  = operation
        self.operand    = operand
        if from_query is not None:
            self.model  = from_query.model
        elif model is not None:
            self.model  = model
        elif operand is not None:
            raise NotImplemented('We also can get model from field data')
        else:
            raise AttributeError('Query requires model to be specified')

    def __and__(self, operand):
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
