"""Test cases for block and extend template tags
"""

BASE = """<!DOCTYPE html>
<html>
<head>
  <title>{{ title }}</title>
  {% block head %}{% endblock %}
</head>
<body>
  {% block content %}Some contents{% endblock %}
</body>
</html>"""
BASE_RESULT = """<!DOCTYPE html>
<html>
<head>
  <title>%s</title>
</head>
<body>
  Some contents
</body>
</html>"""
EXTEND = """{% extend "base.html" %}
{% block head %}<style></style>{% endblock %}
{% block content %}<h1>Hello, world!</h1>{% endblock %}"""
EXTEND_RESULT = """<!DOCTYPE html>
<html>
<head>
  <title>%s</title>
  <style></style>
</head>
<body>
  <h1>Hello, world!</h1>
</body>
</html>"""
 

import unittest

from lighty.templates import Template


def fuzzy_equals(first, second):
    """Check two multiline strings for equality as stripped lines exclude 
    zero-length lines
    """
    make_repr = lambda text: [line.strip() for line in text.split("\n")
                                if len(line.strip()) > 0]
    first_repr = make_repr(first)
    second_repr = make_repr(second)

    if len(first_repr) != len(second_repr):
        return False
    length = len(first_repr)

    i = 0
    while i < length:
        if first_repr[i] != second_repr[i]:
            return False
        i += 1
    
    return True


class BlockTestCase(unittest.TestCase):
    """Test case for block template tag
    """

    def setUp(self):
        self.base_template = Template(name='base.html')
        self.base_template.parse(BASE)

    def testExecuteTemplate(self):
        result =self.base_template.execute({'title': 'Hello'})
        needed = BASE_RESULT % ('Hello')
        is_eq = fuzzy_equals(result, needed)
        assert is_eq, "Error template execution:\n%s" % (
                      "\n".join((result, "except", needed)))


class ExtendTestCase(BlockTestCase):
    """Test case for extend template tag
    """

    def setUp(self):
        super(ExtendTestCase, self).setUp()
        self.extend_template = Template(loader=self.base_template.loader)
        self.extend_template.parse(EXTEND)

    def testExecuteTemplate(self):
        result = self.extend_template.execute({'title': 'Hello'})
        needed = EXTEND_RESULT % ('Hello')
        is_eq = fuzzy_equals(result, needed)
        assert is_eq, "Error template execution:\n%s" % (
                      "\n".join((result, "except", needed)))


def test():
    suite = unittest.TestSuite()
    suite.addTest(BlockTestCase('testExecuteTemplate'))
    suite.addTest(ExtendTestCase("testExecuteTemplate"))
    return suite
