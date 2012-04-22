'''Make functor representation that helps to make queries and another lazy
evaluations
'''
import operator


class BaseField(object):
    '''Base field class
    '''

    def __init__(self):
        super(BaseField, self).__init__()

    def create_functor(self, operator, operand):
        return FieldFunctor(self, operator, operand)

    def __lt__(self, other):
        return self.create_functor(operator.__lt__, other)

    def __gt__(self, other):
        return self.create_functor(operator.__gt__, other)

    def __le__(self, other):
        return self.create_functor(operator.__le__, other)

    def __ge__(self, other):
        return self.create_functor(operator.__ge__, other)

    def __eq__(self, other):
        return self.create_functor(operator.__eq__, other)

    def __ne__(self, other):
        return self.create_functor(operator.__ne__, other)

    def __add__(self, other):
        return self.create_functor('+', other)


class NumericField(BaseField):
    '''Base class for any numerical fields. It can be used to create:

        integers
        floats
        decimals
    '''
    def __sub__(self, other):
        return self.create_functor(operator.__sub__, other)

    def __mul__(self, other):
        return self.create_functor(operator.__mul__, other)

    def __div__(self, other):
        return self.create_functor(operator.__div__, other)

    def __mod__(self, other):
        return self.create_functor(operator.__mod__, other)

    def __pow__(self, other):
        return self.create_functor(operator.__pow__, other)


class SequenceField(BaseField):
    '''Class used for sequences fields creations. It can be used to create:

        strings
        arrays
        dictionaries
    '''
    def __len__(self):
        return 'len'

    def __getitem__(self, key):
        return self.create_functor(operator.__getitem__, key)

    def __contains__(self, item):
        return self.create_functor(operator.__contains__, item)


class FieldFunctor(BaseField):
    '''Class used to keep operations history
    '''
    __slots__ = ('parent', 'operator', 'operand', 'model', )

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

    def __and__(self, other):
        return self.create_functor(operator.__and__, other)

    def __or__(self, other):
        return self.create_functor(operator.__or__, other)

    def __xor__(self, other):
        return self.create_functor(operator.__xor__, other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(%s %s %s)' % (str(self.parent),
                               self.operator, str(self.operand))
