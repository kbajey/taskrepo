from pyramid.response import Response
from pyramid.view import view_config
from searchit.modules import elasticsearch_util

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
    # print elasticsearch_util.get_es_url()
    # print elasticsearch_util.get_es_url_for_id(0)
    # print elasticsearch_util.get_es_host()
    return Response('Search keys')
