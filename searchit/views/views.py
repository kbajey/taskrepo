from pyramid.response import Response
from pyramid.view import view_config
from searchit.modules import es_aggregation_count_util
import datetime

@view_config(route_name='hello')
def hello_world(request):
    return Response('Hello')

@view_config(route_name='hello.json', renderer='json')
def hello_world_json(request):
    data = request.GET.get('page')
    if data:
        print "Data present"
    return {'a':1,'b':2, 'c':3, 'd':[1,2,3,4]}

@view_config(route_name='top_keywords', renderer='json')
def get_top_searched_keywords(request):
	'''
	Returns top searched keywords in a given date range
	'''
	from_date = request.GET.get('from_date')
	to_date = request.GET.get('to_date')
	result = es_aggregation_count_util.get_aggcount_for_date_range(from_date, to_date, range_field='user_visit_time_date', aggs_field='keyword',aggs_size=10)
	return result

@view_config(route_name='top_customers', renderer='json')
def get_top_customers_by_search_count(request):
	'''
	Returns top customers based on number of searches for them,
	in a given date range
	'''
	from_date = request.GET.get('from_date')
	to_date = request.GET.get('to_date')
	result = es_aggregation_count_util.get_aggcount_for_date_range(from_date, to_date, range_field='user_visit_time_date', aggs_field='customer_id',aggs_size=10)
	return result

@view_config(route_name='top_users', renderer='json')
def get_top_users_by_search_count(request):
	'''
	Returns top users based on number of searches performed by them,
	in a given date range
	'''
	from_date = request.GET.get('from_date')
	to_date = request.GET.get('to_date')
	result = es_aggregation_count_util.get_aggcount_for_date_range(from_date, to_date, range_field='user_visit_time_date', aggs_field='user_id',aggs_size=10)
	return result

@view_config(route_name='top_keywords_by_user', renderer='json')
def get_top_keywords_searched_by_user(request):
	'''
	Returns top keywords searched by a particular user
	'''
	user_id = request.GET.get('user_id')
	result = es_aggregation_count_util.get_aggcount_for_field('user_id', user_id, aggs_field='keyword', aggs_size=10)
	return result
    
@view_config(route_name='test_response', renderer='searchit:templates/test_response.mako')
def get_test_response(request):
    '''
    Returns the graph data
    '''
    date_data = request.matchdict['date']
    dt = datetime.datetime.strptime('20141022', '%Y%m%d').strftime('%Y-%m-%d')
    
    first_data = [['DATE', 'Oneill', 'Gander'],['20141018',  220, 360],['20141019',  280,      560],['20141020',  270,       457],
          ['20141021',  285,      356]]
    second_data = [['DATE', 'Oneill', 'Gander'],['20141018',  620, 724],['20141019',  580,      621],['20141020',  770,       627],
          ['20141021',  585,      623]]
    third_data = [['DATE', 'Oneill', 'Gander'],['20141018',  770, 920],['20141019',  670,      870],['20141020',  746,       930],
          ['20141021',  645,      643]]
    return {'date_from': dt, 'data1': first_data, 'data2': second_data, 'data3': third_data}
