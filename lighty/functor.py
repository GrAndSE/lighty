'''Class implements base functor operations
'''
import functools

from .utils import with_metaclass


def create_operator(operator):
    '''Create operator function
    '''
    @functools.wraps(operator)
    def wrap(self, operand):
        '''Call class method to make an operator copy
        '''
        return self.create_copy(operator, operand)
    return wrap


class FunctorBase(type):
    '''Metaclass used to create a classes includes method to generate lazy
    methods to access
    '''

    def __new__(mcs, name, bases, attrs):
        '''Create new class includes lazy methods to override an operators
        '''
        super_new = super(FunctorBase, mcs).__new__
        parents = [b for b in bases if isinstance(b, FunctorBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(mcs, name, bases, attrs)
        # Analyse an attributes
        new_attrs = {'_lazy': set(attrs.get('_lazy', []))}
        for parent in parents:
            if hasattr(parent, '_lazy'):
                new_attrs['_lazy'] |= set(parent._lazy)
        for attr in new_attrs['_lazy']:
            attrs[attr.__name__] = create_operator(attr)
        new_attrs.update(attrs)
        return super_new(mcs, name, bases, new_attrs)


class BaseFunctor(with_metaclass(FunctorBase)):
    '''Base lazy object class
    '''

    def create_copy(self, operator, operand):
        '''Create object's copy
        '''
        raise NotImplementedError('"%s" does not overrides create_copy()'
                                  'method' % self.__class__.__name__)
