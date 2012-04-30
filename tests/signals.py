'''Test case for configuration reader
'''
import unittest

from lighty.signals import SignalDispatcher


class SignalsTestCase(unittest.TestCase):
    '''Test case for signals implementation
    '''

    def setUp(self):
        self.dispatcher = SignalDispatcher()
        self.objects = None
        self.filtered = None

        def handler(objects):
            self.objects = objects

        def filtered(objects):
            self.filtered = objects

        self.dispatcher.channel('/test/', handler)
        self.dispatcher.channel('/args/', handler)
        self.dispatcher.channel('/args/', filtered, filters=[lambda x: x > 0])

    def testEmptySignal(self):
        '''Test handler applied for signal with no objects passed
        '''
        self.dispatcher.signal('/test/')
        assert self.objects == [], (
                'Error dispatchin signal with no objects: %s' % self.objects)

    def testObjectsSignal(self):
        '''Test handler with objects passed into signals
        '''
        self.dispatcher.signal('/args/', [0, 1, 2, 3])
        assert self.objects == [0, 1, 2, 3], (
                'Error dispatchin signal with objects: %s' % self.objects)
        assert self.filtered == [1, 2, 3], ('Error dispatchin signal with '
                'objects filtered: %s' % self.filtered)

def test():
    suite = unittest.TestSuite()
    suite.addTest(SignalsTestCase('testEmptySignal'))
    suite.addTest(SignalsTestCase('testObjectsSignal'))
    return suite
