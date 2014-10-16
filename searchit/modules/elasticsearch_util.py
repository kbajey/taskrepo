import pyramid
INDEX_NAME = 'search_index'
INDEX_TYPE = 'search'

def get_es_url(index_name=INDEX_NAME, index_type=INDEX_TYPE):
    settings = pyramid.threadlocal.get_current_registry().settings
    es_host = settings['ES_HOST']
    es_url = 'http://%s:9200/%s/%s/_search' % (es_host, index_name, index_type)
    return es_url

def get_es_url_for_id(id_val, index_name=INDEX_NAME, index_type=INDEX_TYPE):
    settings = pyramid.threadlocal.get_current_registry().settings
    es_host = settings['ES_HOST']
    es_url = 'http://%s:9200/%s/%s/%s' % (es_host, index_name, index_type, str(id_val))
    return es_url


def get_es_host():
    settings = pyramid.threadlocal.get_current_registry().settings
    es_host = settings['ES_HOST']
    return es_host