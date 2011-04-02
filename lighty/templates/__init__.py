""" Pakage provides method to working with templates """

from loaders import TemplateLoader as Loader
from template import Template as BaseTemplate

from templatetags import *

TemplateLoader = Loader
Template = BaseTemplate
