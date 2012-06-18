'''Define class for getting and storing data
'''
import datetime
import operator

import bson

from ..utils import string_types
from .fields import Field
from .functor import FieldFunctor


class Datastore(object):
    ''' Class used to get and put data into database
    '''
    __slots__ = ('name', 'db_name', 'db', 'get', 'put', )

    def __init__(self, name, db_name, **kwargs):
        from pymongo import Connection
        connection = Connection()
        self.name = name
        self.db_name = db_name
        self.db = connection[db_name]

    def get(self, model, kwargs):
        '''Get item using number of arguments
        '''
        if '_id' in kwargs:
            kwargs['_id'] = bson.objectid.ObjectId(kwargs['_id'])
        return self.db[model.entity_name()].find_one(kwargs)

    def put(self, model, item):
        '''Put item into datastore
        '''
        if '_id' in item:
            item['_id'] = bson.objectid.ObjectId(item['_id'])
        return self.db[model.entity_name()].save(item)

    def delete(self, model, **kwargs):
        return self.db[model.entity_name()].remove(kwargs)

    @staticmethod
    def get_datastore_operation(operation, operand=None):
        '''Get representation of operation for datastore query
        '''
        operator_matching = {
                operator.__or__: '(%s || %s)',
                operator.__and__: '(%s && %s)',
                operator.__not__: '!(%s)',
                operator.__gt__: '(%s > %s)',
                operator.__lt__: '(%s < %s)',
                operator.__ge__: '(%s >= %s)',
                operator.__le__: '(%s <= %s)',
                operator.__eq__: '(%s == %s)',
                operator.__contains__: (
                                    '(%s && (new RegExp(%s, "ig")).exec(%s))'
                                    if isinstance(operand, string_types)
                                    else '(%s && %s.indexOf(%s) > -1)')
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
        elif isinstance(operand, (int, float)):
            return operand
        elif issubclass(operand.__class__, Field):
            return 'this["%s"]' % operand.name
        elif issubclass(operand.__class__, FieldFunctor):
            parent = Datastore.process_operand(operand.parent)
            operator_str = Datastore.get_datastore_operation(operand.operator,
                                                             operand.operand)
            operand_value = Datastore.process_operand(operand.operand)
            if operand.operator == operator.__contains__:
                if isinstance(operand, string_types):
                    return operator_str % (parent, parent, operand_value)
                else:
                    return operator_str % (parent, operand_value, parent)
            return operator_str % (parent, operand_value)
        elif isinstance(operand, bson.objectid.ObjectId):
            return '"%s"' % operand
        elif isinstance(operand, datetime.datetime):
            return (operand.strftime('ISODate("%Y-%m-%dT%H:%M:%S.%%sZ")') %
                    operand.strftime('%f')[:3])
        elif isinstance(operand, datetime.date):
            return operand.strftime('ISODate("%Y-%m-%dT00:00:00.000Z")')
        elif isinstance(operand, datetime.time):
            return operand.strftime('"%H:%M:%S"')
        elif isinstance(operand, (list, tuple)):
            return '["%s"]' % ', '.join([Datastore.process_operand(op)
                                         for op in operand])
        else:
            print operand, type(operand)
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
                return (Datastore.get_datastore_operation(query.operation) %
                        Datastore.process_operand(query.operand),
                        distinct, order)
            return operand, distinct, order
        return (operation % (source_query, operand), distinct, order)

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


class DatastoreManager(object):
    '''Class used to assign database connections to names
    '''

    def __init__(self, default_name='default'):
        self.datastores = {}
        self.default_name = default_name

    def connect(self, name, **kwargs):
        '''Create a connection to database
        '''
        if 'db_name' not in kwargs:
            kwargs['db_name'] = name
        datastore = Datastore(name, **kwargs)
        self.datastores[name] = datastore
        return datastore

    def get(self, name=None):
        '''Get datastore with name specified
        '''
        return self.datastores[name or self.default_name]

    @property
    def default(self):
        '''Default datastore
        '''
        return self.datastores[self.default_name]

    def swap(self, first_name, second_name=None):
        '''Swaps two datastores with specified name
        '''
        if not second_name:
            second_name = self.default_name
        db = self.datastores[first_name].db
        self.datastores[first_name].db = self.datastores[second_name].db
        self.datastores[second_name].db = db


manager = DatastoreManager()
