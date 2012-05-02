'''Define class for getting and storing data
'''
import operator
from ..utils import string_types
from .fields import Field
from .functor import FieldFunctor


class Datastore(object):
    ''' Class used to get and put data into database
    '''
    __slots__ = ('name', 'db_name', 'db', 'get', 'put', )

    def __init__(self, name, db_name):
        from pymongo import Connection
        connection = Connection()
        self.name = name
        self.db_name = db_name
        self.db = connection[db_name]

    def get(self, model, **kwargs):
        '''Get item using number of arguments
        '''
        return self.db[model.entity_name()].find_one(kwargs)

    def put(self, model, item):
        '''Put item into datastore
        '''
        return self.db[model.entity_name()].save(item)

    def delete(self, model, **kwargs):
        return self.db[model.entity_name()].remove(kwargs)

    @staticmethod
    def get_datastore_operation(operation):
        operator_matching = {
                operator.__or__: '||',
                operator.__and__: '&&',
                operator.__not__: '!',
                operator.__gt__: '>',
                operator.__lt__: '<',
                operator.__ge__: '>=',
                operator.__le__: '<=',
                operator.__eq__: '=='
        }
        return operator_matching[operation]

    @staticmethod
    def process_operand(operand):
        if operand is None:
            return ''
        elif isinstance(operand, bool):
            return str(operand).lower()
        elif isinstance(operand, string_types):
            return '"%s"' % operand
        elif isinstance(operand, int):
            return operand
        elif isinstance(operand, float):
            return operand
        elif issubclass(operand.__class__, Field):
            return 'this.' + operand.name
        elif issubclass(operand.__class__, FieldFunctor):
            parent = Datastore.process_operand(operand.parent)
            operator = Datastore.get_datastore_operation(operand.operator)
            operand = Datastore.process_operand(operand.operand)
            return "(%s %s %s)" % (parent, operator, operand)
        else:
            raise AttributeError('Unsupported type %s' % str(type(operand)))

    @staticmethod
    def build_query(query):
        operation = Datastore.get_datastore_operation(query.operation)
        operand = Datastore.process_operand(query.operand)
        if query._from_query is None:
            source_query, distinct, order = '', query.dist, query.order
        else:
            source_query, distinct, order = Datastore.build_query(
                                                            query._from_query)
        if not source_query:
            if operation == operator.__not__:
                return ('%s (%s)' % (
                            Datastore.get_datastore_operation(query.operation),
                            Datastore.process_operand(query.operand)),
                        distinct, order)
            return operand, distinct, order
        return ('(%s) %s %s' % (source_query, operation, operand),
                distinct, order)

    def query(self, query, fields=None):
        items = (fields is None and self.db[query.model.entity_name()].find()
                 or self.db[query.model.entity_name()].find({},
                            dict([(field_name, 1) for field_name in fields])))
        query_string, distinct, order = Datastore.build_query(query)
        if query_string:
            items = items.where(query_string)
        items = distinct and items.distinct('_id') or items
        return order and items.sort([(f.name, 1) for f in order]) or items

    def count(self, query):
        return self.query(query).count()

    def slice(self, query, limit=1, offset=0):
        return self.query(query).skip(offset).limit(limit)


datastore = Datastore('test', 'test')
