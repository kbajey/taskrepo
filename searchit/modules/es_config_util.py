import pyramid
import logging
import datetime
import ConfigParser
import urllib2
import requests
import json
logger = logging.getLogger('searchit')
def get_app_settings(section):
    '''
    Returns a section from ini file as dictionary
    '''
    try:
        config = ConfigParser.ConfigParser()
        config.read('./development.ini')
        es_data = dict(config.items(section))
        return es_data
    except:
        logger.error('Error parsing config file')

def get_es_url(query_type):
    '''
    Returns elasticsearch url required for running queries
    '''
    #settings = get_app_settings('es_settings')
    settings = pyramid.threadlocal.get_current_registry().settings
    if settings:
        es_url = "http://%s:%s/%s/%s/" % (settings['es_host'], settings['es_port'], settings['es_search_index'], settings['es_search_type'])
        if query_type:
            es_url += query_type
            return es_url
    else:
        logger.warning('No settings found for elasticsearch')
    return None

def get_doc_count(query_string):
    '''
    Returns the count of matching documents in elasticsearch
    '''
    es_url = get_es_url('_count')
    if es_url and query_string:
        try:
            es_conn = urllib2.urlopen(es_url, json.dumps(query_string))
            es_doc = es_conn.read()
            es_doc_dict = json.loads(es_doc)
            es_conn.close()
            if es_doc_dict:
                return es_doc_dict['count']
        except Exception,e:
            logging.error('count query failed')
    return None
