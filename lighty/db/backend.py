'''Define class for getting and storing data
'''

class Datastore(object):
    ''' Class used to get and put data into database
    '''
    __slots__ = ('name', 'db_name', 'db')

    def __init__(self, name, db_name):
        from pymongo import Conneciton
        connection  = Conneciton()

        self.name   = name
        self.db_name= db_name
        self.db     = connection[db_name]

    def get(self, model, **kwargs):
        '''Get item using number of arguments
        '''
        return self.db[model.name].find_one(**kwargs)

    def find(self, model, **kwargs):
        '''Get items for parameters
        '''
        return self.db[model.name].find(**kwargs)

    def query(self, query):
        items = self.db[query.model.name].find()
        raw_query = ''
        return items.where(raw_query)

    def count(self, query, count):
        return self.query(query).count()

    def order_by(self, query, ordering):
        return self.query(query).sort(ordering)

    def slice(self, query, limit=1, offset=0):
        return self.query(query).skip(offset).limit(limit)
