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

    return render_template('mod_feed/feed.html', articles=articles, all_articles=all_articles)


@mod_main.route('/<string:article_type>/<int:skip_posts_number>/<int:posts_per_page>', methods=['GET', 'POST'])
def feed_filter(article_type, skip_posts_number, posts_per_page):
    if request.method == 'GET':
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type=article_type, skips=skip_posts_number, limits=posts_per_page)
        all_articles = dumps(articles_cursor)
        return render_template('mod_feed/feed.html', all_articles=all_articles, article_type=article_type)
    elif request.method == 'POST':
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type=article_type, skips=skip_posts_number, limits=posts_per_page)
        all_articles = dumps(articles_cursor)
        return all_articles


@mod_main.route('/articles/search/<string:article_type>/<int:skip_posts_number>/<int:posts_per_page>', methods=['GET', 'POST'])
def search_filter(article_type, skip_posts_number, posts_per_page):
    if request.method == 'GET':
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type=article_type, skips=skip_posts_number, limits=posts_per_page)
        all_articles = dumps(articles_cursor)
        return render_template('mod_feed/search_articles.html', all_articles=all_articles, article_type=article_type)
    elif request.method == 'POST':
        articles_cursor = content_mongo_utils.get_articles_by_type(article_type=article_type, skips=skip_posts_number, limits=posts_per_page)
        all_articles = dumps(articles_cursor)
        return all_articles


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

    return render_template('mod_feed/search.html', organizations=organizations, user_avatar=user_avatar)


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
    return render_template('mod_feed/search_articles.html', articles=articles, user_avatar=user_avatar, get_avatar_url=get_avatar_url)


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
    return render_template('mod_feed/search_people.html', users=users, user_avatar=user_avatar)


def user_avatar(username):
    avatar_url = user_mongo_utils.get_user_by_username(username).avatar_url
    return avatar_url

def get_avatar_url(org_slug):
    organization = org_mongo_utils.get_org_by_slug(org_slug)
    return organization['avatar_url']