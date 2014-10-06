from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='hello')
def hello_world(request):
    return Response('Hello')

@view_config(route_name='hello.json', renderer='json')
def hello_world_json(request):
    data = request.GET.get('page')
    if data:
        print "Data present"
    return {'a':1,'b':2, 'c':3, 'd':[1,2,3,4]}

@view_config(route_name='search')
def search_keys(request):
    return Response('Search keys')
