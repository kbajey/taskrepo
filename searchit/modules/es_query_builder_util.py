from searchit.modules import es_config_util

def get_field_query_object(query_field, query_value):
    '''
    Returns an object for querying against a field
    '''
    field_query_object = {"query":{"match":{query_field:query_value}}}
    return field_query_object

def get_range_object(field_name, from_val, to_val):
    '''
    Returns an object for range operation on a field between a given range
    '''
    range_object = {"range": {field_name: {"from": from_val,"to": to_val}}}
    return range_object

def get_terms_aggregate(field_name, aggs_size=10):
    '''
    Returns an object to run aggregrate on a given field
    '''
    aggs_name = "search%s" % field_name
    aggs_object = {"aggs": {aggs_name: {"terms":{"field": field_name,"size":aggs_size}}}}
    return aggs_object

def get_range_aggregation_query_object(from_val, to_val,
        range_field, aggs_field, aggs_size, size=0):
    '''
    Returns a query object to perform a range operation,
    followed by aggregration on aggs_field
    '''
    range_object = get_range_object(range_field, from_val, to_val)
    aggs_object = get_terms_aggregate(aggs_field,aggs_size)
    query_object = {"size": size, "query":range_object}
    query_object.update(aggs_object)
    return query_object

def get_field_aggregation_query_object(query_field, query_value,
        aggs_field, aggs_size,size=0):
    '''
    Returns a query object that does a match against a field:value,
    followed by aggregration on aggs_field
    '''
    aggs_object = get_terms_aggregate(aggs_field,aggs_size)
    field_query_object = get_field_query_object(query_field,query_value)
    query_object = {"size": size}
    query_object.update(field_query_object)
    query_object.update(aggs_object)
    return query_object
