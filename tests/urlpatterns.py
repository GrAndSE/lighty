from lighty.wsgi.handler import static_patterns
from lighty.wsgi.urls import url

def hello(request):
    return 'Hello, world'

urlpatterns = (url('/hello', hello), ) + static_patterns
