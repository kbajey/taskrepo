import re
import json
import gzip
import urllib2
import random

search_log = gzip.open("./search_sample_log.gz","r")

es_config = {'es_host':'localhost', 'es_port':'9200', 'es_index':'logs', 'es_type':'search'}

# form elastic search query url using elasticsearch config
def get_es_url(es_config,query_type):
    es_url = "http://%s:%s/%s/%s/" % (es_config['es_host'], es_config['es_port'], es_config['es_index'], es_config['es_type'])
    if query_type:
        es_url += query_type
        return es_url
    return None

# get the count of matching documents from elasticsearch
def get_doc_count_from_es(query_string):
    global es_config
    es_url = get_es_url(es_config,'_count')
    if es_url and query_string:
        es_conn = urllib2.urlopen(es_url, query_string)
        es_doc = es_conn.read()
        es_doc_dict = json.loads(es_doc)
        if es_doc_dict:
            return es_doc_dict['count']
    return None

# insert document to elasticsearch
def insert_doc_to_es(search_doc,doc_id):
    global es_config
    if doc_id:
        es_url = get_es_url(es_config,doc_id)
        if es_url and search_doc:
            req = urllib2.Request(es_url,search_doc)
            resp = urllib2.urlopen(req)

# check whether the string is in valid json format or not
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

# extract the search keyword from json string
def get_search_keyword(keyword_string):
    result = json.loads(keyword_string)
    if result:
        return result.values()[0]
    return None

# get customer_id from json data
def get_customer_id_from_utma(utma):
    customer_id = utma.split('-')
    if customer_id:
        return customer_id[0]
    return None

# get user specific information from parsed json data
def get_user_info_utma(utma,customer_id):
    customer_id += '-'
    user_data = utma.split('.')
    user_info = {}
    if user_data and len(user_data) is 4:
        # strip customer_id from beginning to get the actual user_id
        user_data[0] = user_data[0].replace(customer_id,'')
        
        # replacing hypen with underscore sinec hypen is a special character,
        # and it is causing issues with GET _count query
        user_info['user_id'] = user_data[0].replace('-','_')

        user_info['user_creation_time'] = user_data[1]
        user_info['user_visit_time'] = user_data[2]
        user_info['visit_count'] = user_data[3]
        return user_info
    return None

# extract the json data needed from search logs
def get_search_data(line):
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

# create a unique id for each elasticsearch document using userid
def get_unique_doc_id_from_user_id(user_id):
    count_query = json.dumps({"query":{"term":{"user_id":user_id}}})
    doc_count = get_doc_count_from_es(count_query)
    if doc_count is not None:
        doc_count += 1
        doc_id = str(doc_count)+'_'+user_id
        print doc_count
        return doc_id
    return None

# send all the information needed to be logged as document in elasticsearch
def get_search_info_to_insert(search_data):
    search_info = {}
    customer_id = get_customer_id_from_utma(search_data.get('utma'))
    keyword = get_search_keyword(search_data.get('value'))
    if customer_id is None or keyword is None:
        return None
    user_info = get_user_info_utma(search_data.get('utma'),customer_id)

    if user_info:
        search_info['customer_id'] = customer_id
        search_info['user_id'] = user_info['user_id'].replace('-','\-')
        search_info['user_creation_time'] = user_info['user_creation_time']
        search_info['user_visit_time'] = user_info['user_visit_time']
        search_info['visit_count'] = user_info['visit_count']
        search_info['ip'] = search_data.get('ip')
        search_info['user_expiry_time'] = search_data.get('t')
        search_info['keyword'] = keyword
        return search_info

    return None

# do actual insertion in elasticsearch
def insert_search_data_in_es(search_doc,user_id):
    if search_doc and user_id:
        doc_id = get_unique_doc_id_from_user_id(user_id)
        if doc_id:
            insert_doc_to_es(search_doc,doc_id)
        else:
            print 'doc_id is None'
    else:
        print 'No Document to insert or user_id not found'


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

