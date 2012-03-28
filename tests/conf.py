'''Test case for configuration reader
'''
import unittest

from lighty.conf import Settings


class ConfTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''

    def setUp(self):
        self.settings = Settings('tests/test.cfg')

    def testGetFromMainConf(self):
        '''Test getting options from main config file
        '''
        assert self.settings.value == 'test', (
                'Get returns wrong value %s except test' % self.settings.value)
        assert self.settings.value == self.settings.get('value'), (
                '__getitem__ and get returns different values')
        assert self.settings.VALUE == '2', 'Lower case error'

    def testGetFromSection(self):
        '''Check getting option value from section
        '''
        assert self.settings.get('value', 'DEFAULTS') == 'test', (
                'Error on getting value from DEFAULTS section')

    def testConfsLoaded(self):
        '''Test is config files was loaded properly
        '''
        assert self.settings.app_var == '2', 'CONFS was not loaded properly'
        assert self.settings.get('app_var', 'APP1') == '1', (
                'APPS configs was not loaded')
        assert self.settings.get('app_var', 'APP2') == '2', (
                'APPS configs was not loaded')

    def testAppLoaded(self):
        '''Test is application was loaded
        '''
        assert self.settings.test == 'value', 'APPS configs was not loaded'


def test():
    suite = unittest.TestSuite()
    suite.addTest(ConfTestCase('testGetFromMainConf'))
    suite.addTest(ConfTestCase('testGetFromSection'))
    suite.addTest(ConfTestCase('testAppLoaded'))
    suite.addTest(ConfTestCase('testConfsLoaded'))
    return suite
