'''Make functor representation that helps to make queries and another lazy
evaluations
'''
import functools
import operator


class BaseFunctor(object):
    '''Base lazy object class
    '''

    def create_copy(self, operator, operand):
        '''Create object's copy
        '''
        raise NotImplemented('"%s" does not overrides create_copy() method' %
                             self.__class__.__name__)


def create_operator(operator):
    '''Create operator function
    '''
    @functools.wraps(operator)
    def wrap(self, operand):
        return self.create_copy(operator, operand)
    return wrap


class FunctorBase(type):
    '''Metaclass used to create a classes includes method to generate lazy
    methods to access
    '''

    def __new__(mcls, name, bases, attrs):
        '''Create new class includes lazy methods to override an operators
        '''
        super_new = super(FunctorBase, mcls).__new__
        parents = [b for b in bases if isinstance(b, FunctorBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(mcls, name, bases, attrs)
        # Analyse an attributes
        new_attrs = {'_lazy': set(attrs['_lazy']) if '_lazy' in attrs
                              else set()}
        for parent in parents:
            if hasattr(parent, '_lazy'):
                new_attrs['_lazy'] |= set(parent._lazy)
        for attr in new_attrs['_lazy']:
            attrs[attr.__name__] = create_operator(attr)
        new_attrs.update(attrs)
        return super_new(mcls, name, bases, new_attrs)


class BaseField(object):
    '''Base field class
    '''
    __metaclass__ = FunctorBase
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
    _lazy = (operator.__sub__, operator.__mul__, operator.__div__,
             operator.__mod__, operator.__pow__, )


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
