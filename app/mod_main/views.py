from flask import Blueprint, render_template, url_for, request
from app import content_mongo_utils, org_mongo_utils, user_mongo_utils
from bson.json_util import dumps

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET'])
def feed():
    ''' Renders the App index page.
    :return:
    '''
    articles_cursor = content_mongo_utils.get_paginated_articles(0, 6)
    articles = dumps(articles_cursor)

    all_articles_cursor = content_mongo_utils.get_paginated_all_articles(0,6)
    all_articles = dumps(all_articles_cursor)

    # TODO: Create a macro for jinja where you can get avatar link by username
    return render_template('mod_feed/feed.html', articles=articles, all_articles=all_articles)


@mod_main.route('/<string:article_type>', methods=['GET'])
def feed_filter(article_type):

    if article_type == "text":
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type="text", skips=0, limits=8)
        all_articles = dumps(articles_cursor)
    elif article_type == "video":
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type="video", skips=0, limits=8)
        all_articles = dumps(articles_cursor)
    elif article_type == "audio":
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type="audio", skips=0, limits=8)
        all_articles = dumps(articles_cursor)
    elif article_type == "attachment":
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type="attachment", skips=0, limits=8)
        all_articles = dumps(articles_cursor)

    return render_template('mod_feed/feed.html', all_articles=all_articles, article_type=article_type)


@mod_main.route('/organizations/search', methods=['GET'])
def search_organizations():
    ''' Renders the Search organizations page.
    :return:
    '''

    keyword = request.args.get('q')

    if keyword:

        organizations = org_mongo_utils.find_org(keyword)

    else:
        organizations = org_mongo_utils.get_organizations()

    return render_template('mod_feed/search.html', organizations=organizations)


@mod_main.route('/articles/search', methods=['GET'])
def search_articles():
    ''' Renders the Search Articles page.
    :return:
    '''
    keyword = request.args.get('q')

    if keyword:

        articles = content_mongo_utils.find_article(keyword)
    else:
        # TODO: Show latest 10 from each category
        articles = content_mongo_utils.get_articles()
    return render_template('mod_feed/search_articles.html', articles=articles)


@mod_main.route('/people/search', methods=['GET'])
def search_people():
    ''' Renders the Search people page.
    :return:
    '''
    keyword = request.args.get('q')

    if keyword:

        users = user_mongo_utils.find_user(keyword)

    else:

        users = user_mongo_utils.get_users()
    return render_template('mod_feed/search_people.html', users=users)

