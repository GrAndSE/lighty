'''Make functor representation that helps to make queries and another lazy
evaluations
'''
import operator

from .. import functor
from ..utils import string_types


class BaseField(functor.BaseFunctor):
    '''Base field class
    '''
    # Declare lazy operations
    _lazy = (operator.__lt__, operator.__gt__, operator.__le__,
             operator.__ge__, operator.__eq__, operator.__ne__,
             operator.__add__, )

    def __init__(self):
        super(BaseField, self).__init__()

    def create_copy(self, operation, operand):
        return FieldFunctor(self, operation, operand)


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

    def contains(self, operand):
        '''Check is object contains
        '''
        return self.create_copy(operator.__contains__, operand)

    def __len__(self):
        return 'len'


class FieldFunctor(BaseField):
    '''Class used to keep operations history
    '''
    __slots__ = ('parent', 'operator', 'operand', 'model', )
    # Lazy operators
    _lazy = (operator.__and__, operator.__or__, operator.__xor__, )

    def __init__(self, parent, operation, operand):
        super(FieldFunctor, self).__init__()
        if (issubclass(operand.__class__, BaseField) and
            not (issubclass(parent.model.__class__, operand.model.__class__) or
                 issubclass(operand.model.__class__, parent.model.__class__))):
            raise AttributeError('Different model classes %s and %s for '
                                 'operator %s' % (parent.model,
                                 operand.model, operation))
        self.parent = parent
        self.operator = operation
        self.operand = operand
        self.model = parent.model

    def __repr__(self):
        '''Get string representation
        '''
        return '<FieldFunctor: "%s">' % self.__str__()

    def __str__(self, model=None):
        '''Convert to string
        '''
        if model:
            parent = (self.parent.__str__(model)
                      if isinstance(self.parent, FieldFunctor)
                      else str(self.parent))
            datastore = model.datastore()
            operation = datastore.get_datastore_operation(self.operator)
            operand = (self.operand.__str__(model)
                       if isinstance(self.operand, FieldFunctor)
                       else datastore.process_operand(self.operand))
            if self.operator == operator.__contains__:
                if isinstance(operand, string_types):
                    return operation % (parent, parent, operand)
                else:
                    return operation % (parent, operand, parent)
            return operation % (parent, operand)
        return '(%s %s %s)' % (self.parent, self.operator, self.operand)
