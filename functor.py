class Field(object):
    '''Base field class
    '''

    def __init__(self):
        super(Field, self).__init__()

    # Logical operators

    def __and__(self, other):
        print 'And'

    def __or__(self, other):
        print 'Or'

    def __xor__(self, other):
        print 'Xor'

    # Numeric

    def __add__(self, other):
        print '+'

    def __sub__(self, other):
        print '-'

    def __mul__(self, other):
        print '*'

    def __div__(self, other):
        print '/'

    def __mod__(self, other):
        print '%'

    def __pow__(self, other):
        print '**'

    # Comparision

    def __lt__(self, other):
        print '<'

    def __gt__(self, other):
        print '>'

    def __le__(self, other):
        print '<='

    def __ge__(self, other):
        print '>='

    def __eq__(self, other):
        print '=='

    def __ne__(self, other):
        print '!='

    def __nonzero__(self, other):
        print 'bool'

    # Sequences

    def __len__(self):
        print 'len'

    def __getitem__(self, key):
        print '[%s]' % key

    def __contains__(self, item):
        print item, 'in'

    def __getslice__(self, i, j):
        print '[%d:%s]' % (i, j)
