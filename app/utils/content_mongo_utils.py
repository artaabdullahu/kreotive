import datetime
from bson.objectid import ObjectId
from bson.json_util import json


class ContentMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.content_collection = 'content'
        self.users_collection = 'users'

    def add_article(self, content):
        """ Insert article to the database.
         :param content: JSON object containing the content params
         :rtype: Boolean
        """
        self.mongo.db[self.content_collection] \
            .insert(content)
        return True

    def get_articles(self):
        """ Get articles from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True, 'delete': False}).sort([("_id", -1)])

        return articles

    def get_articles_by_type(self, article_type, skips, limits):

        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True, 'delete': False, "type": article_type}).sort([("_id", -1)]).limit(limits).skip(skips)

        articles_dump = list(articles)

        for article in articles_dump:
            avatar_url = self.mongo.db[self.users_collection] \
                .find_one({"username": article['username']})
            if avatar_url:
                article['avatar_url'] = avatar_url['avatar_url']
        return articles_dump

    def get_org_articles(self, org_slug):
        """ Get articles from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'author.org_slug': org_slug, 'author.type': 'organization','visible': True, 'published': True, 'delete': False}).sort([("_id", -1)])

        return articles

    def get_all_org_articles(self, org_slug):
        """ Get articles from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'author.org_slug': org_slug, 'author.type': 'organization','published': True, 'delete': False}).sort([("_id", -1)])

        return articles

    def get_type_org_articles(self, org_slug, article_type):

        articles = self.mongo.db[self.content_collection] \
            .find(
            {'author.org_slug': org_slug, 'author.type': 'organization', 'published': True, 'delete': False, 'type': article_type}).sort(
            [("_id", -1)])

        return articles

    def find_article(self, keyword):
        """ Find articles from the database.
        :param keyword: the keyword we want to search based on.
        :rtype: MongoDB Cursor with all the articles
        """
        find_result = self.mongo.db[self.content_collection].find({'$text': {'$search': keyword}})
        return find_result

    def delete_article(self, slug, delete):
        """ Delete article from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        update = self.mongo.db[self.content_collection] \
            .update({"slug": slug}, {'$set': {"delete": True}});

        return update

    def search(self, text):
        """ Search articles from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'$text': {'$search': text}})

        return articles

    def get_paginated_articles(self, skips, limits):
        """ Get paginated articles from the database.
        :rtype: JSON with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True, 'delete': False, 'post_privacy': 'off'}).sort([("_id", -1)]).limit(limits).skip(skips)

        articles_dump = list(articles)

        for article in articles_dump:
            avatar_url = self.mongo.db[self.users_collection] \
                .find_one({"username": article['username']})
            if avatar_url:
                article['avatar_url'] = avatar_url['avatar_url']
        return articles_dump

    def get_paginated_all_articles(self, skips, limits):
        """ Get paginated articles from the database.
        :rtype: JSON with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True, 'delete': False}).sort([("_id", -1)]).limit(limits).skip(skips)

        articles_dump = list(articles)

        for article in articles_dump:
            avatar_url = self.mongo.db[self.users_collection] \
                .find_one({"username": article['username']})
            if avatar_url:
                article['avatar_url'] = avatar_url['avatar_url']
        return articles_dump


    def get_authors_paginated_articles(self, username, skips, limits):
        """ Get paginated articles from the database for a specific author.
        :rtype: MongoDB Cursor with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({"username": username, 'visible': True, 'published': True, 'delete': False}).sort(
            [("_id", -1)]).limit(limits).skip(skips)

        articles_dump = list(articles)
        for article in articles_dump:
            if article is not None:
                article['avatar_url'] = self.mongo.db[self.users_collection] \
                    .find_one({"username": article['username']})['avatar_url']
        return articles_dump

    def get_org_paginated_articles(self, org_slug, skips, limits):

        articles = self.mongo.db[self.content_collection] \
            .find({"author.org_slug": org_slug, 'visible': True, 'published': True, 'delete': False}).sort(
            [("_id", -1)]).limit(limits).skip(skips)
        articles_dump = list(articles)
        for article in articles_dump:
            if article is not None:
                article['avatar_url'] = self.mongo.db[self.users_collection] \
                    .find_one({"username": article['username']})['avatar_url']
        return articles_dump

    def get_org_public_articles(self, org_slug, skips, limits):
        articles = self.mongo.db[self.content_collection] \
            .find({"author.org_slug": org_slug, 'visible': True, 'published': True, 'delete': False, "post_privacy" : "off"}).sort(
            [("_id", -1)])
        articles_dump = list(articles)
        for article in articles_dump:
            if article is not None:
                article['avatar_url'] = self.mongo.db[self.users_collection] \
                    .find_one({"username": article['username']})['avatar_url']
        return articles_dump

    def get_single_article(self, slug):
        """ Get an article based on the title slug.
        :param slug: the slug version of the title
        :rtype: MongoDB cursor of the founded article.
        """
        articles = self.mongo.db[self.content_collection] \
            .find_one({"slug": slug})
        return articles

    def get_authors_articles(self, username):
        """ Get an article based on the author id.
        :param author_id: the id of the author who wrote the article
        :rtype: MongoDB cursor of the founded article.
        """
        articles = self.mongo.db[self.content_collection] \
            .find({"username": username, 'delete': False}).sort([("_id", -1)])
        return articles

    def change_article_visibility(self, slug, visible):
        """ Update the article to make it show/not show in the feed.
        :param slug: the id of the article we want to change the visibility of
        :param visible: True or False
        :rtype: Boolean
        """
        if visible == 'True':
            update = self.mongo.db[self.content_collection] \
                .update({"slug": slug}, {'$set': {"visible": True}})
        elif visible == 'False':
            update = self.mongo.db[self.content_collection] \
                .update({"slug": slug}, {'$set': {"visible": False}})
        return update

    def count_articles(self, username):
        nr_articles = self.mongo.db[self.content_collection] \
            .find({"username": username, 'visible': True, 'published': True, 'delete': False}).count()
        return nr_articles

    def count_org_articles(self, org_slug):
        nr_articles = self.mongo.db[self.content_collection] \
            .find({"author.org_slug": org_slug, 'visible': True, 'published': True, 'delete': False}).count()
        return nr_articles

    def get_categories(self):
        list_of_categories = self.mongo.db[self.content_collection].distinct("category")
        return list_of_categories

    def count_articles_by_category(self, username, category):

        list_of_categories = self.mongo.db[self.content_collection].distinct("category")
        articles_number_category_list = {}
        for category in list_of_categories:
            nr_articles_category = self.mongo.db[self.content_collection] \
                .find({"username": username, "category": category, 'visible': True, 'published': True,
                       'delete': False}).count()

            articles_number_category_list[category] = nr_articles_category
        return json.dumps(articles_number_category_list)

    def count_org_articles_by_category(self, org_slug, category):

        list_of_categories = self.mongo.db[self.content_collection].distinct("category")
        articles_number_category_list = {}
        for category in list_of_categories:
            nr_articles_category = self.mongo.db[self.content_collection] \
                .find({"author.org_slug": org_slug, "category": category, 'visible': True, 'published': True,
                       'delete': False}).count()

            articles_number_category_list[category] = nr_articles_category
        return json.dumps(articles_number_category_list)

    def get_articles_one_category_only(self, username, category):

        articles = self.mongo.db[self.content_collection] \
            .find({"username": username, "category": category, 'visible': True, 'published': True, 'delete': False})
        return articles

    def get_articles_one_category_only_org(self, org_slug, category, skips, limits):

        articles = self.mongo.db[self.content_collection] \
            .find(
            {"author.org_slug": org_slug, "category": category, 'visible': True, 'published': True, 'delete': False}).sort(
            [("_id", -1)]).limit(limits).skip(skips)

        articles_dump = list(articles)
        for article in articles_dump:
            if article is not None:
                article['avatar_url'] = self.mongo.db[self.users_collection] \
                    .find_one({"username": article['username']})['avatar_url']
        return articles_dump
        return articles_dump
