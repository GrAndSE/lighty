'''Test case for monads and monoidic functions
'''
import unittest

from lighty import monads


class MonadTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''

    def testNumberComparision(self):
        monad = monads.ValueMonad(10)
        assert monad == 10, 'Number __eq__ error: %s' % monad
        assert monad > 9, 'Number __gt__ error: %s' % monad
        assert monad >= 10, 'Number __ge__ error: %s' % monad
        assert monad < 11, 'Number __lt__ error: %s' % monad
        assert monad <= 10, 'Number __le__ error: %s' % monad

    def testNumberActions(self):
        monad = monads.ValueMonad(10)
        assert monad + 10 == 20, 'Number + error: %s' % (monad + 10)
        assert monad - 5 == 5, 'Number - error: %s' % (monad - 5)
        assert monad / 2 == 5, 'Number / error: %s' % (monad / 2)
        assert monad * 2 == 20, 'Number * error: %s' % (monad * 2)
        assert monad ** 2 == 100, 'Number pow error: %s' % (monad ** 2)
        assert monad << 1 == 10 << 1, 'Number << error: %s' % (monad << 1)
        assert monad >> 1 == 10 >> 1, 'Number >> error: %s' % (monad >> 1)

    def testNumberSeq(self):
        monad = monads.ValueMonad(10)
        assert len(monad) == 1, 'Number len error: %s' % len(monad)
        assert monad[0] == 10, 'Number [0] error: %s' % monad[0]
        assert isinstance(monad[1], monads.NoneMonad), ('Number [1] error' %
                monad[1])
        assert not 10 in monad, 'Number in error: %s' % (10 in monad)


def test():
    suite = unittest.TestSuite()
    suite.addTest(MonadTestCase('testNumberComparision'))
    suite.addTest(MonadTestCase('testNumberActions'))
    suite.addTest(MonadTestCase('testNumberSeq'))
    return suite
