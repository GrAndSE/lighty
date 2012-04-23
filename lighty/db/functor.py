'''Make functor representation that helps to make queries and another lazy
evaluations
'''
import operator

from .. import functor


class BaseField(functor.BaseFunctor):
    '''Base field class
    '''
    # Declare lazy operations
    _lazy = (operator.__lt__, operator.__gt__, operator.__le__,
             operator.__ge__, operator.__eq__, operator.__ne__,
             operator.__add__, )

    def __init__(self):
        super(BaseField, self).__init__()

    def create_copy(self, operator, operand):
        return FieldFunctor(self, operator, operand)


class NumericField(BaseField):
    '''Base class for any numerical fields. It can be used to create:

        integers
        floats
        decimals
    '''
    _lazy = (operator.__sub__, operator.__mul__, operator.__truediv__,
             operator.__floordiv__, operator.__mod__, operator.__pow__, )


class SequenceField(BaseField):
    '''Class used for sequences fields creations. It can be used to create:

        strings
        arrays
        dictionaries
    '''
    _lazy = (operator.__getitem__, operator.__contains__, )

    def __len__(self):
        return 'len'


class FieldFunctor(BaseField):
    '''Class used to keep operations history
    '''
    __slots__ = ('parent', 'operator', 'operand', 'model', )
    # Lazy operators
    _lazy = (operator.__and__, operator.__or__, operator.__xor__, )

    def __init__(self, parent, operator, operand):
        super(FieldFunctor, self).__init__()
        if (issubclass(operand.__class__, BaseField) and
                parent.model != operand.model):
            raise AttributeError('Different model classes %s and %s for '
                                 'operator %s' % (parent.model,
                                 operand.model, operator))
        self.parent = parent
        self.operator = operator
        self.operand = operand
        self.model = parent.model

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(%s %s %s)' % (str(self.parent), self.operator.__name__,
                               str(self.operand))
