from pyramid.response import Response
from pyramid.view import view_config
from searchit.modules import es_aggregation_count_util

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
