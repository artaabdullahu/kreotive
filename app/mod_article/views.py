from flask import Blueprint, render_template, request, Response, redirect, url_for
from app import content_mongo_utils, profile_mongo_utils, org_mongo_utils, user_mongo_utils, bookmarks_mongo_utils
from flask.ext.security import current_user
from slugify import slugify
from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

mod_article = Blueprint('article', __name__, url_prefix='/article')


@mod_article.route('/<slug>', methods=['GET'])
def article(slug):
    # TODO: Restrict access to only authenticated users if the article has "visible" set to False
    article = content_mongo_utils.get_single_article(slug)
    is_bookmarked = bookmarks_mongo_utils.get_bookmark_article(current_user.username, article["slug"])
    profile = None
    organization = None
    if article:
        if article['author']['type'] == 'individual':
            profile = profile_mongo_utils.get_profile(article['author']['slug'])
        elif article['author']['type'] == 'organization':
            organization = org_mongo_utils.get_org_by_slug(article['author']['org_slug'])
    else:
        article = None
    return render_template('mod_article/article_single.html', is_bookmarked=is_bookmarked, user_avatar=user_avatar,
                           article=article, profile=profile, organization=organization)


@mod_article.route('/articles/organization/<organization_slug>/<string:article_action>')
def organization_articles(organization_slug, article_action):
    message = None
    if article_action == "save":
        message = "Your article has been saved, but not published."
    elif article_action == "publish":
        message = "Your article has been published."
    elif article_action == "show":
        message = "Showing your latest articles"

    # TODO: Restrict access to only authenticated users
    organization = org_mongo_utils.get_org_by_slug(organization_slug)
    articles = content_mongo_utils.get_all_org_articles(organization_slug)
    return render_template('mod_article/organization_article_management.html', organization=organization,
                           articles=articles, article_action=article_action,
                           message=message)


@mod_article.route('/articles/organization/<organization_slug>/<string:article_action>/<string:article_type>')
def organization_articles_type(organization_slug, article_action, article_type):
    message = None
    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    if article_type == "text":
        articles = content_mongo_utils.get_type_org_articles(organization_slug, article_type="text")
        message = "Showing organization text articles"
    elif article_type == "video":
        message = "Showing organization video articles"
        articles = content_mongo_utils.get_type_org_articles(organization_slug, article_type="video")
    elif article_type == "audio":
        message = "Showing organization audio articles"
        articles = content_mongo_utils.get_type_org_articles(organization_slug, article_type="audio")
    elif article_type == "attachment":
        message = "Showing organization attachment articles"
        articles = content_mongo_utils.get_type_org_articles(organization_slug, article_type="attachment")

    # TODO: Restrict access to only authenticated users

    return render_template('mod_article/organization_article_management.html', organization=organization,
                           articles=articles, article_action=article_action,
                           message=message, article_type=article_type)


@mod_article.route('/user/<username>')
def authors_articles(username):
    # TODO: Restrict access to only authenticated users
    articles = content_mongo_utils.get_authors_articles(username)
    return render_template('mod_article/article_management.html', articles=articles)


@mod_article.route('/my-articles/<string:article_action>')
def my_articles(article_action):
    message = None
    if article_action == "save":
        message = "Your article has been saved, but not published."
    elif article_action == "publish":
        message = "Your article has been published."
    elif article_action == "show":
        message = "Showing your latest articles"
    elif article_action == 'delete':
        message = "Article/s deleted."
    # TODO: Restrict access to only authenticated users
    articles = content_mongo_utils.get_authors_articles(current_user.username)
    profile = user_mongo_utils.get_user_by_username(current_user.username)
    return render_template('mod_article/article_management.html', profile=profile, articles=articles,
                           article_action=article_action,
                           message=message)


@mod_article.route('/<string:author_type>/<string:username>/new', methods=["POST", "GET"])
def new_article(author_type, username):
    organization = None
    if author_type == 'organization':
        organization = org_mongo_utils.get_org_by_slug(username)

    if request.method == "GET":

        return render_template('mod_article/write_article.html', organization=organization)
    elif request.method == "POST":
        form = request.form
        if author_type == "individual":
            new_article_from_author(form, username)
            return redirect(url_for('article.my_articles', article_action='show'))
        if author_type == "organization":
            new_article_from_org(form, username, organization)
            return redirect(url_for('article.organization_articles', organization_slug=organization['org_slug'],
                                    article_action='show'))


def new_article_from_author(form, username):
    action = form['action']
    content = form['content']
    category = form['category']
    title = form['title']
    type = form['type']
    post_privacy = ''
    if 'post-privacy' in form:
        post_privacy = form['post-privacy']
    else:
        post_privacy = 'off'
    publish_article = True
    delete = False
    if action == "save":
        publish_article = False
    elif action == "cancel":
        return redirect(url_for('article.my_articles', article_action='show'))
    content_mongo_utils.add_article({
        "content": content,
        "visible": publish_article,
        "category": category,
        "title": title,
        "slug": slugify(title) + '-' + str(ObjectId()),
        "type": type,
        "username": current_user.username,
        "published": publish_article,
        "post_privacy": post_privacy,
        "delete": delete,
        "published_date": datetime.now(),
        "author": {
            "type": "individual",
            "slug": username,
            "name": current_user.name,
            "lastname": current_user.lastname
        }
    })
    return redirect(url_for('article.my_articles', article_action='save'))


def new_article_from_org(form, username, organization):
    action = form['action']
    content = form['content']
    category = form['category']
    title = form['title']
    type = form['type']
    post_privacy = ''
    if 'post-privacy' in form:
        post_privacy = form['post-privacy']
    else:
        post_privacy = 'off'
    publish_article = True
    delete = False
    if action == "save":
        publish_article = False
    elif action == "cancel":
        return redirect(
            url_for('article.organization_articles', organization_slug=organization['org_slug'], article_action='show'))
    content_mongo_utils.add_article({
        "content": content,
        "visible": publish_article,
        "category": category,
        "title": title,
        "slug": slugify(title) + '-' + str(ObjectId()),
        "type": type,
        "username": current_user.username,
        "published": publish_article,
        "delete": delete,
        "post_privacy": post_privacy,
        "published_date": datetime.now(),
        "author": {
            "type": "organization",
            "org_slug": organization['org_slug'],
            "org_name": organization['name'],
            "name": current_user.name,
            "lastname": current_user.lastname
        }
    })
    return redirect(
        url_for('article.organization_articles', organization_slug=organization['org_slug'], article_action='save'))


@mod_article.route('/visibility/<slug>/<visible>', methods=["POST", "GET"])
def edit_article_visibility(slug, visible):
    update = content_mongo_utils.change_article_visibility(slug, visible)
    return redirect(url_for('article.my_articles', article_action='show'))


@mod_article.route('/visibility/organization/<string:organization_slug>/<string:slug>/<string:visible>',
                   methods=["POST", "GET"])
def edit_org_article_visibility(slug, visible, organization_slug):
    organization = org_mongo_utils.get_org_by_slug(organization_slug)
    update = content_mongo_utils.change_article_visibility(slug, visible)
    return redirect(
        url_for('article.organization_articles', organization_slug=organization['org_slug'], article_action='show'))


@mod_article.route('/articles/<int:skip_posts_number>/<int:posts_per_page>', methods=['POST'])
def paginated_articles(skip_posts_number, posts_per_page):
    # TODO: Restrict access to only authenticated users
    articles = dumps(content_mongo_utils.get_paginated_articles(skip_posts_number, posts_per_page))

    return Response(response=articles)


@mod_article.route('/articles/<string:username>/<int:skip_posts_number>/<int:posts_per_page>', methods=['POST'])
def paginated_author_articles(username, skip_posts_number, posts_per_page):
    # TODO: Restrict access to only authenticated users
    articles = dumps(content_mongo_utils.get_authors_paginated_articles(username, skip_posts_number, posts_per_page))

    return Response(response=articles)


@mod_article.route('/articles/<string:organization_slug>/<int:skip_posts_number>/<int:posts_per_page>',
                   methods=['POST'])
def paginated_org_articles(organization_slug, skip_posts_number, posts_per_page):
    # TODO: Restrict access to only authenticated users
    articles = dumps(
        content_mongo_utils.get_org_paginated_articles(organization_slug, skip_posts_number, posts_per_page))

    return Response(response=articles)


@mod_article.route('/delete/<slug>/<delete>', methods=["POST", "GET"])
def delete_article(slug, delete):
    # TODO: Restrict access to only authenticated users
    article = content_mongo_utils.delete_article(slug, delete)
    return redirect(url_for('article.my_articles', article=article, article_action='show'))


@mod_article.route('/bookmark/add', methods=["POST", "GET"])
def bookmark_article():
    bookmark = bookmarks_mongo_utils.bookmark_article(request.form['username'], request.form['slug'])

    return redirect(url_for('article.article', username=request.form['username'], slug=request.form['slug']))


def user_avatar(username):
    avatar_url = user_mongo_utils.get_user_by_username(username).avatar_url
    return avatar_url


@mod_article.route('/bookmark/remove', methods=["POST"])
def remove_bookmark():
    remove_bookmark = bookmarks_mongo_utils.remove_bookmark(request.form['username'], request.form['slug'])

    return redirect(url_for('article.article', username=request.form['username'], slug=request.form['slug'],
                            remove_bookmark=remove_bookmark))
