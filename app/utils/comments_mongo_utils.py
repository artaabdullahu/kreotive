import datetime
from bson.objectid import ObjectId
from bson import _bson_to_dict
from bson.json_util import loads
from datetime import datetime
from bson.json_util import dumps


class CommentsMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.comments_collection = 'comments'
        self.content_collection = 'content'
        self.users_collection = 'users'

    def add_comment(self, slug, text, username, first_name, last_name):
        """ Insert comment to the database.
         :param comment: Text field containing comment string.
         :rtype: Boolean
        """
        comment = {
            "username": username,
            "firstname": first_name,
            "lastname": last_name,
            "slug": slug,
            "text": text,
            "date": datetime.utcnow()
        }
        comment_id = self.mongo.db[self.comments_collection] \
            .insert(comment)
        return comment_id

    def add_comment_reply(self, reply_of, slug, text, username, first_name, last_name):
        """ Insert comment to the database.
         :param comment: Text field containing comment string.
         :rtype: Boolean
        """
        comment = {
            "username": username,
            "firstname": first_name,
            "lastname": last_name,
            "slug": slug,
            "text": text,
            "reply_of": ObjectId(reply_of),
            "date": datetime.utcnow()
        }
        comment_id = self.mongo.db[self.comments_collection] \
            .insert(comment)
        return comment_id

    def get_comments(self, slug):
        """ Insert comment to the database.
         :param article_id: Id of the article
         :rtype: Boolean
        """
        query = {
            "slug": slug
        }
        cursor = self.mongo.db[self.comments_collection] \
            .find(query)

        result = list(cursor)
        results_ = list()
        for elem in result:
            elem['avatar_url'] = \
                self.mongo.db[self.users_collection] \
                    .find_one({"username": elem['username']})['avatar_url']
            results_.append(elem)
        return dumps(results_)


    def get_comments_list(self, username):
        comments = self.mongo.db[self.comments_collection] \
            .find({"username": username}).sort(
            [("_id", -1)])
        return comments

    def get_article_title(self,slug):

        article = self.mongo.db[self.content_collection] \
            .find_one({"slug":slug})

        return article

    def remove_comment(self, username, comment_id):

        comment = self.mongo.db[self.comments_collection] \
            .remove({"username":username, "_id": ObjectId(comment_id)})
        return comment
