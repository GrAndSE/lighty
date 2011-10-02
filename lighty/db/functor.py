class BaseField(object):
    '''Base field class
    '''
    def __init__(self):
        super(BaseField, self).__init__()

    def create_functor(self, operator, operand):
        return FieldFunctor(self, operator, operand)

    def __lt__(self, other):
        return self.create_functor('<', other)

    def __gt__(self, other):
        return self.create_functor('>', other)

    def __le__(self, other):
        return self.create_functor('<=', other)

    def __ge__(self, other):
        return self.create_functor('>=', other)

    def __eq__(self, other):
        return self.create_functor('==', other)

    def __ne__(self, other):
        return self.create_functor('!=', other)

    def __add__(self, other):
        return self.create_functor('+', other)


class NumericField(BaseField):
    '''Base class for any numerical fields. It can be used to create:

        integers
        floats
        decimals
    '''
    def __sub__(self, other):
        return self.create_functor('-', other)

    def __mul__(self, other):
        return self.create_functor('*', other)

    def __div__(self, other):
        return self.create_functor('/', other)

    def __mod__(self, other):
        return self.create_functor('%', other)

    def __pow__(self, other):
        return self.create_functor('**', other)


class SequenceField(BaseField):
    '''Class used for sequences fields creations. It can be used to create:

        strings
        arrays
        dictionaries
    '''
    def __len__(self):
        return 'len'

    def __getitem__(self, key):
        return self.create_functor('[]', key)

    def __contains__(self, item):
        return self.create_functor('in', item)

    def __getslice__(self, i, j):
        return self.create_functor('[%d:%s]', (i, j))


class FieldFunctor(BaseField):
    '''Class used to keep operations history
    '''
    __slots__ = ('parent', 'operator', 'operand', 'model')

    def __init__(self, parent, operator, operand):
        super(FieldFunctor, self).__init__()
        if (issubclass(operand.__class__, BaseField) and 
            parent.model == operand.model):
            raise AttributeError('Different model classes %s and %s for '
                                 'operator %s' % (parent.model,
                                 operand.model, operator))
        self.parent     = parent
        self.operator   = operator
        self.operand    = operand
        self.model      = parent.model

    def __and__(self, other):
        return self.create_functor('and', other)

    def __or__(self, other):
        return self.create_functor('or', other)

    def __xor__(self, other):
        return self.create_functor('xor', other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(%s %s %s)' % (str(self.parent),
                               self.operator, str(self.operand))
