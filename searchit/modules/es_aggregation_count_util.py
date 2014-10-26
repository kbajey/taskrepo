from searchit.modules import es_config_util
from searchit.modules import es_query_builder_util
import json
import urllib2
import logging
import datetime

logger = logging.getLogger('searchit')

def get_aggcount_for_date_range_for_customer(customer, from_val, to_val, range_field='user_visit_time_date',
        aggs_field='keyword',aggs_size=10):
    """
    Aggregates on aggs_field, for a given date range using range_field
    """
    es_url = es_config_util.get_es_url("_search")
    query_object = es_query_builder_util.get_range_aggregation_query_object_for_customer(customer, from_val, to_val,
                                                                                         range_field, aggs_field,
                                                                                         aggs_size)
    # print json.dumps(query_object)
    if es_url and query_object:
        try:
            es_conn = urllib2.urlopen(es_url,json.dumps(query_object))
            es_doc = es_conn.read()
            es_doc_dict = json.loads(es_doc)
            if es_doc_dict:
                aggs_name = "search%s" % aggs_field 
                return es_doc_dict['aggregations'][aggs_name]['buckets']
            es_conn.close()
        except Exception,e:
            logger.error('testing log')
            return "Something went wrong, please try again"

def get_aggcount_for_date_range(from_val, to_val, range_field='user_visit_time_date',
        aggs_field='keyword',aggs_size=10):
    """
    Aggregates on aggs_field, for a given date range using range_field
    """
    es_url = es_config_util.get_es_url("_search")
    query_object = es_query_builder_util.get_range_aggregation_query_object(from_val, to_val, range_field, aggs_field, aggs_size)
    # print json.dumps(query_object)
    if es_url and query_object:
        try:
            es_conn = urllib2.urlopen(es_url,json.dumps(query_object))
            es_doc = es_conn.read()
            es_doc_dict = json.loads(es_doc)
            if es_doc_dict:
            	aggs_name = "search%s" % aggs_field 
                return es_doc_dict['aggregations'][aggs_name]['buckets']
            es_conn.close()
        except Exception,e:
            logger.error('testing log')
            return "Something went wrong, please try again"

def get_aggcount_for_field(query_field='user_id',query_value='',
        aggs_field='keyword',aggs_size=10):
    '''
    Aggregates on aggs_field, after doing a match against query field 
    '''
    es_url = es_config_util.get_es_url("_search")
    query_object = es_query_builder_util.get_field_aggregation_query_object(query_field, query_value, aggs_field, aggs_size)
    if es_url and query_object:
        # print json.dumps(query_object)
        try:
            es_conn = urllib2.urlopen(es_url,json.dumps(query_object))
            es_doc = es_conn.read()
            es_doc_dict = json.loads(es_doc)
            if es_doc_dict:
                aggs_name = "search%s" % aggs_field 
                return es_doc_dict['aggregations'][aggs_name]['buckets']
            es_conn.close()
        except Exception,e:
            return "Something went wrong, please try again"


def get_aggcount_for_customer_id(aggs_size=20):
    '''
    Aggregates on aggs_field, after doing a match against query field
    '''
    es_url = es_config_util.get_es_url("_search")
    query_object = {"size":0, "query": {"match_all":{}}, "aggs":{"customers": {"terms": {"field": "customer_id", "size": 25}}}}
    if es_url and query_object:
        # print json.dumps(query_object)
        try:
            es_conn = urllib2.urlopen(es_url,json.dumps(query_object))
            es_doc = es_conn.read()
            es_doc_dict = json.loads(es_doc)
            if es_doc_dict:
                return es_doc_dict['aggregations']['customers']['buckets']
            es_conn.close()
        except Exception,e:
            return "Something went wrong, please try again"


def main():
	# top 10 keywords for a given date range
    get_aggcount_for_date_range('2014-09-08', '2014-09-10', range_field='user_visit_time_date', aggs_field='keyword', aggs_size=10)
    
    # top 10 customers based on number of searches
    get_aggcount_for_date_range('2014-09-08', '2014-09-10', range_field='user_visit_time_date', aggs_field='customer_id', aggs_size=10)

	#top 10 users for a particular customer based on number of searches
    get_aggcount_for_date_range('2014-09-08', '2014-09-10', range_field='user_visit_time_date', aggs_field='user_id', aggs_size=10)

if __name__ == "__main__":
    main()
