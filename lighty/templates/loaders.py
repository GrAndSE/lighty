"""Package provides template loaders
"""
import itertools
import os
import os.path


class TemplateLoader(object):
    '''Class fot managing templates
    '''

    def __init__(self):
        '''Create new template loader
        '''
        super(TemplateLoader, self).__init__()
        # Create new templates dictionary
        self.templates = {}

    def register(self, name, template):
        '''Add loaded or generated template
        '''
        self.templates[name] = template

    def get_template(self, name):
        '''Get template by name
        '''
        if name not in self.templates:
            raise Exception("Template '%s' was not found" % name)
        return self.templates[name]


class FSLoader(TemplateLoader):
    '''Class provides methods for template managing
    '''

    def __init__(self, template_dirs):
        '''Create new FSLoader instance, retrieves all the templates from
        template dictionaries specified and register them
        '''
        from .template import LazyTemplate
        super(FSLoader, self).__init__()
        for path in template_dirs:
            for root, dirs, files in os.walk(path):
                if root.startswith(path):
                    relative_path = root.replace(path, '')
                else:
                    parts = root.split(path)
                    relative_path = parts[-1]
                if relative_path.startswith('/'):
                    relative_path = relative_path[1:]
                for file_name in files:
                    name = os.path.join(relative_path, file_name)
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        content = itertools.chain(*file.readlines())
                        LazyTemplate(content, name=name, loader=self)
