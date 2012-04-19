from lighty.wsgi.decorators import view
from lighty.wsgi.static import static_patterns
from lighty.wsgi.urls import url


@view
def hello(request):
    return 'Hello, world'

urlpatterns = (url('/hello', hello), ) + static_patterns
