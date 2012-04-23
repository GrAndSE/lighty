'''Class implements base functor operations
'''
import functools


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


class BaseFunctor(object):
    '''Base lazy object class
    '''
    __metaclass__ = FunctorBase

    def create_copy(self, operator, operand):
        '''Create object's copy
        '''
        raise NotImplemented('"%s" does not overrides create_copy() method' %
                             self.__class__.__name__)
