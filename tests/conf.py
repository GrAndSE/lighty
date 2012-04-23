'''Test case for configuration reader
'''
import unittest

from lighty.conf import Settings

TEST_APPS = ['benchmark', 'lighty.db', 'lighty.templates', 'lighty.wsgi',
             'tests']


class ConfTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''

    def setUp(self):
        self.settings = Settings('tests/test.cfg')

    def testGetFromMainConf(self):
        '''Test getting options from main config file'''
        assert self.settings.value == 'test', (
                'Get returns wrong value %s except test' % self.settings.value)
        assert self.settings.value == self.settings.get('value'), (
                '__getitem__ and get returns different values')
        assert self.settings.VALUE == 'test', 'Lower case error'

    def testGetFromSection(self):
        '''Check getting option value from section'''
        assert self.settings.get('value', 'DEFAULTS') == 'test', (
                'Error on getting value from DEFAULTS section')

    def testConfsLoaded(self):
        '''Test is config files was loaded properly'''
        assert self.settings.app_var == '2', 'CONFS was not loaded properly'
        assert self.settings.get('app_var', 'APP1') == '1', (
                'APPS configs was not loaded')
        assert self.settings.get('app_var', 'APP2') == '2', (
                'APPS configs was not loaded')

    def testAppLoaded(self):
        '''Test is application was loaded'''
        assert self.settings.test == 'value', 'APPS configs was not loaded'

    def testSections(self):
        '''Test is all values in sections'''
        apps_req = TEST_APPS
        apps = sorted(self.settings.section('APPS'))
        assert apps == apps_req, ('APPS section was not loaded properly: %s' %
                                  apps)
        assert self.settings.section('APP1') == ['app_var'], (
                'APP1 section was not loaded properly: %s' %
                self.settings.section('APP1'))
        assert self.settings.section('APP2') == ['app_var'], (
                'APP2 section was not loaded properly: %s' %
                self.settings.section('APP1'))
        assert sorted(self.settings.section('CONFS')) == [
                'tests/conf/app1.cfg', 'tests/conf/app2.cfg'], (
                        'CONFS section was not loaded properly')


def test():
    suite = unittest.TestSuite()
    suite.addTest(ConfTestCase('testGetFromMainConf'))
    suite.addTest(ConfTestCase('testGetFromSection'))
    suite.addTest(ConfTestCase('testAppLoaded'))
    suite.addTest(ConfTestCase('testConfsLoaded'))
    suite.addTest(ConfTestCase('testSections'))
    return suite
