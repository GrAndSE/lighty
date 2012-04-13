import functools

from .handler import handler
from .urls import load_urls, resolve


def WSGIApplication(app_settings):
    '''Create main application handler
    '''

    class Application(object):
        settings = app_settings
        urls = load_urls(settings.urls)
        resolve_url = functools.partial(resolve, urls)

    return functools.partial(handler, Application, Application.resolve_url)
