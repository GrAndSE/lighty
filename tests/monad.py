'''Test case for monads and monoidic functions
'''
import unittest

from lighty import monads


class MonadTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''

    def testNumberComparision(self):
        '''Test comparing monad with number'''
        monad = monads.ValueMonad(10)
        assert monad == 10, 'Number __eq__ error: %s' % monad
        assert monad > 9, 'Number __gt__ error: %s' % monad
        assert monad >= 10, 'Number __ge__ error: %s' % monad
        assert monad < 11, 'Number __lt__ error: %s' % monad
        assert monad <= 10, 'Number __le__ error: %s' % monad

    def testNumberActions(self):
        '''Test monad numeric operations'''
        monad = monads.ValueMonad(10)
        assert monad + 10 == 20, 'Number + error: %s' % (monad + 10)
        assert monad - 5 == 5, 'Number - error: %s' % (monad - 5)
        assert monad / 2 == 5, 'Number / error: %s' % (monad / 2)
        assert monad * 2 == 20, 'Number * error: %s' % (monad * 2)
        assert monad ** 2 == 100, 'Number pow error: %s' % (monad ** 2)
        assert monad << 1 == 10 << 1, 'Number << error: %s' % (monad << 1)
        assert monad >> 1 == 10 >> 1, 'Number >> error: %s' % (monad >> 1)

    def testNumberSeq(self):
        '''Test accessing to number as a scequnce inside monad'''
        monad = monads.ValueMonad(10)
        assert len(monad) == 1, 'Number len error: %s' % len(monad)
        assert monad[0] == 10, 'Number [0] error: %s' % monad[0]
        assert isinstance(monad[1], monads.NoneMonad), ('Number [1] error' %
                monad[1])
        assert not 10 in monad, 'Number in error: %s' % (10 in monad)

    def testSeqActions(self):
        '''Test sequunces operations with monads'''
        monad = monads.ValueMonad([10])
        assert monad + [20] == [10, 20], 'Sequence __eq__ error: %s' % (
                monad + [20])
        assert monad * 2 == [10, 10], 'Sequence * error: %s' % (monad * 2)

    def testSequence(self):
        '''Test monad sequnces accessing'''
        monad = monads.ValueMonad([1, 2, 3, 4])
        assert monad[0] == 1, 'Sequence [0] error: %s' % monad[0]
        assert monad[:2] == [1, 2], 'Sequence [:2] error: %s' % monad[:2]
        assert monad[1:2] == [2], 'Sequence [1:2] error: %s' % monad[1:2]
        assert monad[monads.ValueMonad(2):] == [3, 4], (
                'Sequence [ValueMonad(2):] error: %s' %
                monad[monads.ValueMonad(2):])
        assert isinstance(monad[5], monads.NoneMonad), (
                'Sequence [5] error: %s' % monad[5])
        assert monad[1:monads.ValueMonad(-1)] == [2, 3], (
                'Sequence [1:ValueMonad(-1)] error: %s' %
                monads[1:monads.ValueMonad(-1)])


def test():
    suite = unittest.TestSuite()
    suite.addTest(MonadTestCase('testNumberComparision'))
    suite.addTest(MonadTestCase('testNumberActions'))
    suite.addTest(MonadTestCase('testNumberSeq'))
    suite.addTest(MonadTestCase('testSeqActions'))
    suite.addTest(MonadTestCase('testSequence'))
    return suite
