'''Module contains methods to interact with WSGI
'''
import os

from ..db.backend import manager as db_manager
from ..templates.loaders import FSLoader

from .urls import load_urls, resolve, reverse


class BaseApplication(object):
    '''Base application class contains obly settings, urls and resolve_url
    method
    '''

    def __init__(self, settings):
        self.settings = settings
        self.urls = load_urls(settings.urls)

    def resolve_url(self, url):
        '''Resolve url
        '''
        return resolve(self.urls, url)

    def reverse_url(self, name, args=None):
        '''Reverse url for name and arguments
        '''
        return reverse(self.urls, name, args)


class ComplexApplication(BaseApplication):
    '''Application loads also templates and database connection
    '''

    def __init__(self, settings):
        super(ComplexApplication, self).__init__(settings)
        # process an applications and get a template directories
        apps = settings.section('APPS')
        template_dirs = []
        for app in apps:
            module = __import__(app, globals(), locals(), app.split('.')[-1])
            template_dir = os.path.join(module.__path__[0], 'templates')
            if os.path.exists(template_dir):
                template_dirs.append(template_dir)
        # get template directories from settings
        if settings.has_section('TEMPLATE_DIRS'):
            template_dirs += settings.section_options('TEMPLATE_DIRS')
        self.template_loader = FSLoader(template_dirs)
        # get databse connections
        for section in settings.sections():
            if section.startswith('DATABASE:'):
                name = section.replace('DATABASE:', '')
                args = settings.section(section)
                db_manager.connect(name, **args)

    def get_template(self, name):
        '''Get template for name
        '''
        return self.template_loader.get_template(name)

    def get_datastore(self, name):
        '''Get datastore for name
        '''
        return db_manager.get(name)
