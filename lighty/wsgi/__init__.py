from functools import partial

from .handler import handler
from .urls import load_urls, resolve


def WSGIApplication(settings):
    '''Create main application handler
    '''
    urls = load_urls(settings.urls)
    resolve_url = partial(resolve, urls)
    return partial(handler, resolve_url)
