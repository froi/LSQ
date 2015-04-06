# import pymongo as m
from datetime import datetime
from mongokit import Connection, Document
from bson.objectid import ObjectId

import config

connection = Connection(host=config.mongo_hostname, port=config.mongo_port)

@connection.register
class Query(Document):
    __database__ = 'company_queries'
    __collection__ = 'queries'
    _obj_class = Document  # TODO: find out why an error shows up when this isn't here. Should be inhereted from Document.

    structure = {
        'title': basestring,
        'sql': basestring,
        'tags': [basestring],
        'desc': basestring,
        'who': basestring,
        'date_created': datetime,
        'date_updated': datetime,
    }
    required_fields = ['title', 'sql', 'desc', 'who']
    default_values = {
        'date_created': datetime.utcnow
    }
    use_dot_notation = True

def get_tags_list(tags):
    return [ tag.strip() for tag in tags.strip().split(",") \
            if len(tag.strip()) > 0]

def insert_query(title, sql, tags, desc, who):

    query = connection.Query()
    
    query.title = title
    query.sql = sql
    query.tags = get_tags_list(tags)
    query.desc = desc
    query.who = who
    query.save()
    

def update_query(id, title, sql, tags, desc, who):
    query = connection.Query.find_one(ObjectId(id))
    
    query.title = title
    query.sql = sql
    query.tags = get_tags_list(tags)
    query.desc = desc
    query.who = who
    query.date_updated = datetime.utcnow()

    query.save()

def delete_query(id):
    connection.Query.find_one(ObjectId(id)).delete()
    # queries.remove({"_id": ObjectId(id)})

def get_queries():
    return list(connection.Query.find())

def get_query_details(id):
    return connection.Query.find_one(ObjectId(id))