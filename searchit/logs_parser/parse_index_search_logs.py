import sys
import re
import json
import gzip
import urllib2
import ConfigParser
import logging
import datetime
import requests

def log_error_message(message):
    '''
    Logs the error message in a seperate log file
    '''
    log_file = './parsing_search_logs_' + datetime.datetime.utcnow().date().strftime('%Y-%m-%d') + '.log'
    log_format = '%(asctime)s:%(lineno)d - %(levelname)s %(message)s'
    logging.basicConfig(filename= log_file, format = log_format, level=logging.ERROR)
    logging.error(message)

def get_app_settings(section):
    '''
    Reads a particular section from ini file and returns it as dictionary
    '''
    try:
        config = ConfigParser.ConfigParser()
        config.read('../development.ini')
        es_data = dict(config.items(section))
        return es_data
    except:
        log_error_message('Error parsing config file') 

def get_log_file_path():
    '''
    Gets the path of the log file to be parsed and indexed in ES
    '''
    try:
        settings = get_app_settings('search_log_settings')
        log_directory = settings['log_path']
        log_file = "%s/search_sample_log.gz" % log_directory
        return log_file
    except:
        log_error_message('Error parsing search log file')
    
def search_index_exists():
    '''
    Checks whether search_index already exists, if not then creates it
    '''
    settings = get_app_settings('es_settings')
    es_url = "http://%s:%s/%s" % (settings['es_host'], settings['es_port'], settings['es_search_index'])
    req = requests.head(es_url)
    if req.status_code == 200:
        return True
    else:
        resp = create_search_index()
        return resp
    log_error_message('elasticsearch url is invalid')
    return False

def create_search_index():
    '''
    Creates a new search_index in ES 
    '''
    settings = get_app_settings('es_settings')
    es_url = "http://%s:%s/%s" % (settings['es_host'], settings['es_port'], settings['es_search_index'])
    req = requests.put(es_url)
    if req.status_code == 200:
        return True
    log_error_message('cannot create search_index')
    return False
            
def get_es_url(query_type):
    '''
    Returns elasticsearch url based on query type (e.g _search,_count,doc_id)
    '''
    settings = get_app_settings('es_settings')
    es_url = "http://%s:%s/%s/%s/" % (settings['es_host'], settings['es_port'], settings['es_search_index'], settings['es_search_type'])
    if query_type:
        es_url += query_type
        return es_url
    return None

def get_doc_count_from_es(query_string):
    '''
    Gets the count of matching documents in ES
    '''
    es_url = get_es_url('_count')
    if es_url and query_string:
        es_conn = urllib2.urlopen(es_url, query_string)
        es_doc = es_conn.read()
        es_doc_dict = json.loads(es_doc)
        if es_doc_dict:
            return es_doc_dict['count']
    log_error_message('count query failed')
    return None

def insert_doc_to_es(search_doc,doc_id):
    '''
    Inserts a new document in search_index
    '''
    if doc_id:
        es_url = es_url = get_es_url(doc_id)
        if es_url and search_doc:
            req = urllib2.Request(es_url,search_doc)
            resp = urllib2.urlopen(req)

def is_json(myjson):
    '''
    Checks whether the string is in valid json format or not
    '''
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

def get_search_keyword(keyword_string):
    '''
    Extracts and returns the search keyword from json string
    '''
    result = json.loads(keyword_string)
    if result:
        return result.values()[0]
    return None

def get_customer_id_from_utma(utma):
    '''
    Returns customer_id from utma string
    '''
    customer_id = utma.split('-')
    if customer_id:
        return customer_id[0]
    return None

def get_user_info_utma(utma):
    '''
    Returns all user related information from utma string
    '''
    user_data = utma.split('.')
    user_info = {}
    if user_data and len(user_data) is 4:
        '''
        '-' is a special characted in ES and hence will cause troubling 
        while quering, replacing '-' with '_'
        ''' 
        user_info['user_id'] = user_data[0].replace('-','_')
        user_info['user_creation_time'] = user_data[1]
        user_info['user_visit_time'] = user_data[2]
        user_info['visit_count'] = user_data[3]
        return user_info
    return None

def get_search_data(line):
    '''
    Extracts the json data needed from each line in search log
    '''
    pattern = re.compile("'{(.*)}'")
    if pattern.search(line) is None:
        return None
    search_data = ''.join(pattern.search(line).groups())

    #adding braces to form json string
    search_data = '{'+search_data+'}'

    #the logged format has two backslah (\\), which leads to invalid json
    #chaning (\\) to (\)
    search_data = search_data.replace("\\\\","\\")

    #decode/convert json string to dictionary
    if is_json(search_data): 
        search_data = json.loads(search_data)
        return search_data
    return None

def get_unique_doc_id_from_user_id(user_id):
    '''
    Creates a unique id for each elasticsearch document using userid
    '''
    count_query = json.dumps({"query":{"term":{"user_id":user_id}}})
    doc_count = get_doc_count_from_es(count_query)
    if doc_count is not None:
        doc_count += 1
        doc_id = str(doc_count)+'_'+user_id
        return doc_id
    return None

def get_search_info_to_insert(search_data):
    '''
    Sends all the fields for a document to be stored in elasticsearch
    '''
    search_info = {}
    customer_id = get_customer_id_from_utma(search_data.get('utma'))
    keyword = get_search_keyword(search_data.get('value'))
    if customer_id is None or keyword is None:
        return None
    user_info = get_user_info_utma(search_data.get('utma'))

    user_creation_time_date = get_date_string_from_timestamp(user_info['user_creation_time'])
    user_visit_time_date = get_date_string_from_timestamp(user_info['user_visit_time'])
    user_expiry_time_date = get_date_string_from_timestamp(search_data.get('t'))

    if user_info:
        search_info['customer_id'] = customer_id
        search_info['user_id'] = user_info['user_id'].replace('-','\-')
        search_info['user_creation_time'] = long(user_info['user_creation_time'])
        search_info['user_creation_time_date'] = user_creation_time_date
        search_info['user_visit_time'] = long(user_info['user_visit_time'])
        search_info['user_visit_time_date'] = user_visit_time_date
        search_info['visit_count'] = user_info['visit_count']
        search_info['ip'] = search_data.get('ip')
        search_info['user_expiry_time'] = long(search_data.get('t'))
        search_info['user_expiry_time_date'] = user_expiry_time_date
        search_info['keyword'] = keyword
        return search_info

    return None

def get_date_string_from_timestamp(timestamp):
    '''
    Returns a date in Y-m-d format, given a unix timestamp in milliseconds
    '''
    if timestamp:
        return datetime.datetime.fromtimestamp(float(timestamp)/1000).strftime('%Y-%m-%d')
    log_error_message('Invalid timestamp')
    return None

def insert_search_data_in_es(search_doc,user_id):
    '''
    Inserts a search document in elasticsearch
    '''
    if search_doc and user_id:
        doc_id = get_unique_doc_id_from_user_id(user_id)
        if doc_id:
            insert_doc_to_es(search_doc,doc_id)
        else:
            log_error_message('doc_id is None')
    else:
        log_error_message('No Document to insert or user_id not found')

if __name__ == "__main__":

    if search_index_exists():
        search_log = gzip.open(get_log_file_path(), "r")

        for line in search_log:
            # get the formatted search log data
            search_data = get_search_data(line)
            
            # if we don't have the data or if log type is not seach, skip that line
            if search_data is None or search_data.get('type') != 'search':
                continue
            
            # get the required information that needs to be inserted into elasticsearch
            search_info = get_search_info_to_insert(search_data)
            
            if search_info:    
                search_doc = json.dumps(search_info)

                insert_search_data_in_es(search_doc,search_info['user_id'])
                
        search_log.close()

