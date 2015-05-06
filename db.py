# import pymongo as m
from datetime import datetime
from mongokit import Connection, Document
from bson.objectid import ObjectId
from markdown import markdown

import config

connection = Connection(host=config.mongo_hostname, port=config.mongo_port)

@connection.register
class User(Document):
    __database__ = 'company_snippets'
    __collection__ = 'users'
    _obj_class = Document

    structure = {
        'username': basestring,
        'password': basestring,
        'email': basestring,
        'fname': basestring,
        'lname': basestring,
        'date_created': datetime,
        'last_login': datetime,
    }

    required_fields = ['username', 'password', 'email']
    use_dot_notation = True
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self._id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)


@connection.register
class Comment(Document):
    __database__ = 'company_snippets'
    __collection__ = 'comments'
    _obj_class = Document

    structure = {
        'text': basestring,
        'who': basestring,
        'date_created': datetime,
        'date_updated': datetime,
    }
    required_fields = ['text', 'who']
    use_dot_notation = True


@connection.register
class Snippet(Document):
    __database__ = 'company_snippets'
    __collection__ = 'snippets'
    _obj_class = Document  # TODO: find out why an error shows up when this isn't here. Should be inhereted from Document.

    structure = {
        'title': basestring,
        'text': basestring,
        'type': basestring,
        'tags': [basestring],
        'desc': basestring,
        'who': basestring,
        'date_created': datetime,
        'date_updated': datetime,
        'comments': [Comment]
    }
    required_fields = ['title', 'text', 'type', 'desc', 'who']
    use_dot_notation = True
    use_autorefs = True

def get_tags_list(tags):
    return [ tag.strip() for tag in tags.strip().split(",") \
            if len(tag.strip()) > 0]

def insert_snippet(title, snippet_text, snippet_type, tags, desc, who):

    snippet = connection.Snippet()
    
    snippet.title = title
    snippet.text = snippet_text
    snippet.type = snippet_type
    snippet.tags = get_tags_list(tags)
    snippet.desc = desc
    snippet.who = who
    snippet.date_created = datetime.utcnow()
    snippet.date_updated = datetime.utcnow()
    snippet.save()

def update_snippet(snippet_id, title, sql, tags, desc, who):
    snippet = connection.snippet.find_one(ObjectId(snippet_id))
    
    query.title = title
    query.text = snippet
    query.type = snippet_type
    query.tags = get_tags_list(tags)
    query.desc = desc
    query.who = who
    query.date_updated = datetime.utcnow()

    query.save()

def delete_snippet(snippet_id):
    connection.Snippet.find_one(ObjectId(snippet_id)).delete()

def get_snippets():
    return list(connection.Snippet.find())

def get_snippet_details(snippet_id):
    snippet = connection.Snippet.find_one(ObjectId(snippet_id))
    snippet.desc = markdown(snippet.desc)
    tmp_comments = []

    for comment in query.comments:
        comment.text = markdown(comment.text)
        tmp_comments.append(comment)

    snippet.comments = tmp_comments
    return snippet

def insert_comment(comment_text, who):

    comment = connection.Comment()

    comment.text = comment_text
    comment.who = who
    comment.date_created = datetime.utcnow()
    comment.date_updated = datetime.utcnow()

    comment.save()

    return comment

def update_comment(comment_id, comment_text, who):
    comment = connection.Comment.find_one(ObjectId(comment_id))

    comment.text = comment_text
    comment.who = who
    comment.date_updated = datetime.utcnow()

    comment.save()

def delete_comment(comment_id):
    connection.Comment.find_one(ObjectId(comment_id)).delete()

def get_comments():
    tmp_comments = []
    comments = connection.Comment.find()

    for comment in comments:
        comment.text = markdown(comment.text)
        tmp_comments.append(comment)

    return tmp_comments

def get_user(user_id=None, username=None):
    if user_id:
        user = connection.User.find_one(ObjectId(user_id))
    elif username:
        user = connection.User.find_one({'username': username})
    else:
        pass  # TODO: what to do here...raise error or return None?
    return user

def add_user(username, password, email=None, fname=None, lname=None):
    user = connection.User()

    user.username = username
    user.password = password
    user.email = email
    user.fname = fname
    user.lname = lname

    user.save()