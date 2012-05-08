import functools
import os

from ..templates.loaders import FSLoader

from .handler import handler
from .urls import load_urls, resolve


class BaseApplication(object):
    '''Base application class contains obly settings, urls and resolve_url
    method
    '''

    def __init__(self, settings):
        self.settings = settings
        self.urls = load_urls(settings.urls)
        self.resolve_url = functools.partial(resolve, self.urls)


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
        self.get_template = self.template_loader.get_template
        # get databse connections
        from ..db.backend import manager
        for section in settings.sections():
            if section.startswith('DATABASE:'):
                name = section.replace('DATABASE:', '')
                args = settings.section(section)
                manager.connect(name, **args)


def WSGIApplication(app_settings):
    '''Create main application handler
    '''
    application = ComplexApplication(app_settings)
    return functools.partial(handler, application, application.resolve_url)
