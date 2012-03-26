"""Test cases for block and extend template tags
"""
import unittest

from lighty.templates.loaders import FSLoader

from .blockextend import fuzzy_equals

BASE_RESULT = '''<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8">
	<title>Base template</title>
</head>
<body>
	
</body>
</html>'''
EXTEND_RESULT = '''<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8">
	<title>Index page title</title>
</head>
<body>
	Hello, world!
</body>
</html>'''



class BlockTestCase(unittest.TestCase):
    """Test case for block template tag
    """

    def setUp(self):
        self.loader = FSLoader(['tests/templates'])
        self.base_template = self.loader.get_template('base.html')

    def testExecuteTemplate(self):
        result = self.base_template()
        is_eq = fuzzy_equals(result, BASE_RESULT)
        assert is_eq, "Error template execution:\n%s" % (
                      "\n".join((result, "except", BASE_RESULT)))


class ExtendTestCase(BlockTestCase):
    """Test case for extend template tag
    """

    def setUp(self):
        super(ExtendTestCase, self).setUp()
        self.extend_template = self.loader.get_template('index.html')

    def testExecuteTemplate(self):
        result = self.extend_template()
        is_eq = fuzzy_equals(result, EXTEND_RESULT)
        assert is_eq, "Error template execution:\n%s" % (
                      "\n".join((result, "except", EXTEND_RESULT)))


def test():
    suite = unittest.TestSuite()
    suite.addTest(BlockTestCase('testExecuteTemplate'))
    suite.addTest(ExtendTestCase("testExecuteTemplate"))
    return suite
