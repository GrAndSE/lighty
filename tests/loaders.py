"""Test cases for block and extend template tags
"""
import unittest

from lighty.templates import Template
from lighty.templates.loaders import FileLoader

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
	<title>Index page template</title>
</head>
<body>
	Hello, world!
</body>
</html>'''



class BlockTestCase(unittest.TestCase):
    """Test case for block template tag
    """

    def setUp(self):
        loader = FileLoader('tests/templates.html')
        self.base_template = Template(name='base.html', loader=loader)

    def testExecuteTemplate(self):
        result = self.base_template.execute()
        is_eq = fuzzy_equals(result, BASE_RESULT)
        assert is_eq, "Error template execution:\n%s" % (
                      "\n".join((result, "except", BASE_RESULT)))


class ExtendTestCase(BlockTestCase):
    """Test case for extend template tag
    """

    def setUp(self):
        super(ExtendTestCase, self).setUp()
        self.extend_template = Template(loader=self.base_template.loader,
                                        name='index.html')

    def testExecuteTemplate(self):
        result = self.extend_template.execute()
        is_eq = fuzzy_equals(result, EXTEND_RESULT)
        assert is_eq, "Error template execution:\n%s" % (
                      "\n".join((result, "except", EXTEND_RESULT)))


def test():
    suite = unittest.TestSuite()
    suite.addTest(BlockTestCase('testExecuteTemplate'))
    suite.addTest(ExtendTestCase("testExecuteTemplate"))
    return suite
