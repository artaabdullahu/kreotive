import json

from flask import Blueprint, Response, request, url_for
from app import comment_mongo_util
from datetime import datetime
from app import user_mongo_utils

mod_comments = Blueprint('comments', __name__, url_prefix='/comments')


@mod_comments.route('/add', methods=['POST'])
def add_comment():
    ''' Adds comment.
    :return JSON:
    '''
    username = request.form['username']
    comment_id = comment_mongo_util.add_comment(request.form['slug'], request.form['text'], username,
                                                request.form['firstname'], request.form['lastname'])

    user = user_mongo_utils.get_user_by_username(username)

    response = {"id": str(comment_id), "avatar_url": url_for('static', filename=user.avatar_url)}

    return Response(json.dumps(response), status=200, mimetype='application/json')


@mod_comments.route('/add/reply', methods=['POST'])
def add_comment_reply():
    ''' Adds comment reply.
    :return JSON:
    '''
    data = request.form

    comment_id = comment_mongo_util.add_comment_reply(data['reply_of'], data['slug'], data['text'],
                                                      data['username'],
                                                      data['firstname'], data['lastname'])

    user = user_mongo_utils.get_user_by_username(data['username'])

    response = {"id": str(comment_id), "avatar_url": url_for('static', filename=user.avatar_url)}

    return Response(json.dumps(response), status=200, mimetype='application/json')


@mod_comments.route('/get', methods=['POST'])
def get_comments():
    ''' Returns comments
    :return:
    '''
    comments = comment_mongo_util.get_comments(request.form['slug'])
    return comments
