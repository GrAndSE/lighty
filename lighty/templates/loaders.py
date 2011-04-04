""" Package provides template loaders """


class TemplateLoader(object):
    """ Class fot managing templates """

    def __init__(self, settings=None):
        """ Create new template loader """
        super(TemplateLoader, self).__init__()
        # Create new templates dictionary
        self.templates = {}
        # TODO: do something with settings

    def register(self, name, template):
        """ Add loaded or generated template """
        self.templates[name] = template

    def get_template(self, name):
        """ Get template by name """
        if name not in self.templates:
            raise Exception("Template '%s' was not found" % name)
        return self.templates[name]
