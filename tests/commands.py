'''Test case for configuration reader
'''
import unittest


class CommandsTestCase(unittest.TestCase):
    '''Test case for partial template execution
    '''

    def testLoadCommandsFromApp(self):
        '''Test loading commands for one application
        '''
        from lighty.commands import load_commands_from_app
        cmds = load_commands_from_app('tests')
        assert cmds == [('test', test)], ('Error loading commands for '
                                          'application tests:\n%s' % cmds)
        cmds = load_commands_from_app('lighty.wsgi')
        from lighty.wsgi import commands
        assert cmds == [('make_application', commands.make_application),
                        ('run_server', commands.run_server),
                        ('run_tornado', commands.run_tornado)], (
                                'Error loading commands for '
                                'application lighty.wsgi:\n%s' % cmds)
        cmds = load_commands_from_app('lighty.templates')
        assert cmds == [], ('Error loading commands for application '
                            'lighty.templates:\n%s' % cmds)

    def testLoadCommands(self):
        '''Test loading commands for few applications
        '''
        from lighty.commands import load_commands
        cmds = load_commands(['lighty.wsgi', 'tests'])
        assert sorted(cmds.keys()) == ['make_application', 'run_server',
                                       'run_tornado', 'test'], ('Error loading'
                                ' commands for ["lighty.wsgi","tests"]:\n%s' % 
                                sorted(cmds.keys()))


def test():
    suite = unittest.TestSuite()
    suite.addTest(CommandsTestCase('testLoadCommandsFromApp'))
    suite.addTest(CommandsTestCase('testLoadCommands'))
    return suite
