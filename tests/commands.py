def test(settings, test_name='all'):
    '''Run tests from tests directory
    '''
    import unittest

    runner = unittest.TextTestRunner(verbosity=2)

    name = 'tests.' + test_name
    module = __import__(name, globals(), locals(), 'test')
    function = getattr(module, 'test')
    if not callable(function):
        raise AttributeError('%s.%s is not callable' % (name, 'test'))

    suite = function()
    runner.run(suite)
