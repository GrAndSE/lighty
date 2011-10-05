'''Define class for getting and storing data
'''
from fields import Field
from functor import FieldFunctor
from operations import NOT, AND, OR


class Datastore(object):
    ''' Class used to get and put data into database
    '''
    __slots__ = ('name', 'db_name', 'db')

    def __init__(self, name, db_name):
        from pymongo import Connection
        connection  = Connection()

        self.name   = name
        self.db_name= db_name
        self.db     = connection[db_name]

    def get(self, model, **kwargs):
        '''Get item using number of arguments
        '''
        return self.db[model].find_one(**kwargs)

    def find(self, model, **kwargs):
        '''Get items for parameters
        '''
        return self.db[model].find(**kwargs)

    @staticmethod
    def get_datastore_operation(operation):
        operator_matching = {
                OR:     '||',
                AND:    '&&',
                NOT:    '!',
        }
        return operator_matching[operation]

    @staticmethod
    def process_operand(operand):
        if operand is None:
            return ''
        elif isinstance(operand, basestring):
            return '"%s"' % operand
        elif isinstance(operand, int):
            return operand
        elif isinstance(operand, float):
            return operand
        elif isinstance(operand.__class__, Field):
            return 'this.' + operand.name
        elif issubclass(operand.__class__, FieldFunctor):
            operand = Datastore.process_operand(operand.operand)
            operator= Datastore.get_datastore_operation(operand.operator)
            parent  = Datastore.process_operand(operand.parent)
            return "(%s %s %s)" % (parent, operator, operand)
        else:
            raise AttributeError('Unsupported type %s' % str(type(operand)))

    @staticmethod
    def build_query(query):
        operation   = Datastore.get_datastore_operation(query.operation)
        operand     = Datastore.process_operand(query.operand)
        if query.from_query is None:
            if operation == NOT:
                return '%s (%s)' % (
                            Datastore.get_datastore_operation(query.operation),
                            Datastore.process_operand(query.operand))
            return operand, query.distinct
        source_query, distinct = Datastore.build_query(query.from_query)
        return ('(%s) %s %s' % (source_query, operand, operand), 
                query.distinct | distinct)

    def query(self, query):
        items = self.db[query.model].find()
        query, distinct = Datastore.build_query(query)
        return distinct and items.where(query).distinct('_id') or items.where(query)

    def count(self, query, count):
        return self.query(query).count()

    def order_by(self, query, ordering):
        return self.query(query).sort(ordering)

    def slice(self, query, limit=1, offset=0):
        return self.query(query).skip(offset).limit(limit)


datastore = Datastore('test', 'test')
