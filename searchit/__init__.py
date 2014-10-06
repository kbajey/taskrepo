from pyramid.config import Configurator
from pyramid.view import notfound_view_config, forbidden_view_config
from pyramid.response import Response


@notfound_view_config()
def notfound(request):
    return Response('Not Found, Try something else', status='404 Not Found')

@forbidden_view_config()
def forbidden(request):
    msg = u"Not allowed"
    request.session.flash(msg)
    return Response(angry_message, status='403 Forbidden')

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('hello', '/')
    config.add_route('hello.json', 'hello.json')
    config.add_route('search', 'search')
    config.scan()
    return config.make_wsgi_app()
