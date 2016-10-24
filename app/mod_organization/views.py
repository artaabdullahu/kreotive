from flask import Blueprint, render_template, request, Response, redirect, url_for, send_from_directory
from flask.ext.security import login_required, current_user
from app import org_mongo_utils, content_mongo_utils, user_mongo_utils, upload_folder, uds
from bson.json_util import dumps
import os
from datetime import datetime
from werkzeug.utils import secure_filename

mod_organization = Blueprint('organization', __name__, url_prefix='/organization')


@mod_organization.route('/<organization_slug>', methods=['GET'])
def feed(organization_slug):
    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    feed = dumps(content_mongo_utils.get_org_paginated_articles(organization_slug, 0, 8))

    public_feed = dumps(content_mongo_utils.get_org_public_articles(organization_slug, 0, 8))

    is_member = org_mongo_utils.check_if_user_is_member_of(organization_slug, current_user.username)

    return render_template('mod_organization/feed.html', feed=feed, organization=organization,
                           organization_slug=organization_slug, is_member=is_member, public_feed=public_feed)


@mod_organization.route('/<organization_slug>/<category>', methods=['GET'])
def category_feed_org(organization_slug, category):
    ''' Loads the feed page with specific category article.
            '''

    # get the profile object for the given username

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    feed = dumps(content_mongo_utils.get_articles_one_category_only_org(organization_slug, category, 0, 8))

    is_member = org_mongo_utils.check_if_user_is_member_of(organization_slug, current_user.username)

    return render_template('mod_organization/feed.html', organization=organization, feed=feed,
                           organization_slug=organization_slug, is_member=is_member)


@mod_organization.route('/<organization_slug>/about', methods=['GET'])
def about(organization_slug):
    # feed = None

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    articles_no = content_mongo_utils.count_org_articles(organization_slug)

    is_member = org_mongo_utils.check_if_user_is_member_of(organization_slug, current_user.username)

    followers_no = 0

    members_no = 0

    if 'followers' in organization:
        followers_no = len(organization['followers'])

    if 'members' in organization:
        members_no = len(organization['members'])

    return render_template('mod_organization/about.html', is_member=is_member, organization=organization, feed=feed,
                           organization_slug=organization_slug, articles_no=articles_no, followers_no=followers_no,
                           members_no=members_no)


@mod_organization.route('/<organization_slug>/archive', methods=['GET'])
def archive(organization_slug):
    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    category = content_mongo_utils.get_categories()

    articles_by_category_org = content_mongo_utils.count_org_articles_by_category(organization_slug, category)

    is_member = org_mongo_utils.check_if_user_is_member_of(organization_slug, current_user.username)

    return render_template('mod_organization/archive.html', is_member=is_member, organization=organization,
                           articles_by_category_org=articles_by_category_org)


@mod_organization.route('/<organization_slug>/search', methods=['GET'])
def search(organization_slug):
    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    articles = content_mongo_utils.get_org_articles(organization_slug)

    users = user_mongo_utils.get_users()

    is_member = org_mongo_utils.check_if_user_is_member_of(organization_slug, current_user.username)

    return render_template('mod_organization/search.html', is_member=is_member, organization=organization, feed=feed,
                           articles=articles,
                           users=users)


@mod_organization.route('/<string:organization_slug>/settings', methods=["POST", "GET"])
def organization_settings(organization_slug):
    # Get the profile info

    if request.method == "GET":
        organization = org_mongo_utils.get_org_by_slug(organization_slug)
        return render_template('mod_organization/account.html', organization=organization, error='')
    elif request.method == "POST":
        user_json = {}
        if request.form['org_email'] is not None:
            user_json['email'] = request.form['org_email']
            user_json['name'] = request.form['org_name']
            user_json['location'] = request.form['org_location']
            user_json['telephone'] = request.form['org_telephone']
            user_json['mobile'] = request.form['org_mobile']
            user_json['about_org'] = request.form['about_org']
            org_mongo_utils.update_org({"org_slug": organization_slug}, user_json)
            organization = org_mongo_utils.get_org_by_slug(organization_slug)
        return render_template('mod_organization/account.html', organization=organization,
                               error="Successfully updated organization profile.")


@mod_organization.route('/<organization_slug>/<action>', methods=['POST'])
def follow(organization_slug, action):
    '''
    TODO:
        1. Get POST reuqest body JSON
        2. Get the username of the follower.
        3. Implement org_mongo_utils.add_follower()
        4. Call org_mongo_utils.add_follower()
        5. Check if it adds the follower username in the document.
        6. Implement org_mongo_utils.remove_follower()
    '''
    follower_username = current_user.username
    org_mongo_utils.add_follower(follower_username, organization_slug, action)
    resp = Response(status=200)
    return resp


@mod_organization.route('/<organization_slug>/ask-to-join/<username>', methods=['POST'])
def ask_to_join(organization_slug, username):
    '''
    TODO:
        1. Get POST reuqest body JSON
        2. Get the username of the follower.
        3. Implement org_mongo_utils.add_follower()
        4. Call org_mongo_utils.add_follower()
        5. Check if it adds the follower username in the document.
        6. Implement org_mongo_utils.remove_follower()
    '''
    org_mongo_utils.ask_to_join(username, organization_slug)
    resp = Response(status=200)
    return resp


@mod_organization.route('/<organization_slug>/memberships', methods=['GET'])
def memberships(organization_slug):
    profile = user_mongo_utils.get_users()
    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    pending_approval_members_count = 0
    approved_members_count = 0
    editors_count = 0
    admin_count = 1

    pending_approval_members_list = org_mongo_utils.get_users_by_status(organization_slug, 'pending')
    approved_members_list = org_mongo_utils.get_users_by_status(organization_slug, 'member')
    editors_list = org_mongo_utils.get_users_by_status(organization_slug, 'editor')
    admin_list = org_mongo_utils.get_users_by_status(organization_slug, 'admin')

    if 'members' in pending_approval_members_list:
        pending_approval_members_count = len(pending_approval_members_list['members'])

    if 'members' in approved_members_list:
        approved_members_count = len(approved_members_list['members'])
    if 'members' in editors_list:
        editors_count = len(editors_list['members'])
    if 'members' in admin_list:
        admin_count = len(admin_list['members'])

    total_members_count = editors_count + approved_members_count + admin_count

    is_member = 'org_admin'

    return render_template('mod_organization/memberships.html', profile=profile, organization=organization,
                           user_avatar=user_avatar, pending_approval_count=pending_approval_members_count,
                           approved_members_count=total_members_count,
                           admin_count=admin_count,
                           get_user_name_last_name_by_username=get_user_name_last_name_by_username)


def user_avatar(username):
    avatar_url = user_mongo_utils.get_user_by_username(username).avatar_url
    return avatar_url


@login_required
@mod_organization.route('/upload', methods=["GET", 'POST'])
def upload_avatar(self):
    error = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo' not in request.files:
            error = 'No file part'
            return redirect(request.url)
        file = request.files['photo']
        allowed_file = self.allowed_file(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = 'No selected file'
            return redirect(request.url)
        if file and allowed_file:
            filename = secure_filename(file.filename)
            directory = str(upload_folder) + str(current_user.username) + '/' + str(
                datetime.now().strftime('%Y-%m'))
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(os.path.join(directory, filename))
            photo_url = 'uploads/' + str(current_user.username) + '/' + str(
                datetime.now().strftime('%Y-%m')) + "/" + filename
            user_mongo_utils.change_avatar(current_user.username, photo_url)
            return redirect(url_for('organization.organization_settings',
                                    username=current_user.username))
    return redirect(url_for('organization.organization_settings', username=current_user.username, error=error))


@login_required
@mod_organization.route('/photo/<filename>', methods=["GET"])
def get_avatar_url(self, org_slug):
    organization = org_mongo_utils.get_org_by_slug(org_slug)
    return organization['avatar_url']


# Memberships management
@mod_organization.route('/<organization_slug>/accept/<username>', methods=['POST'])
def accept_member(organization_slug, username):
    org_mongo_utils.accept_member(organization_slug, username)
    return Response(200)


@mod_organization.route('/<organization_slug>/denote/<username>', methods=['POST'])
def denote_member(organization_slug, username):
    org_mongo_utils.denote_member(organization_slug, username)
    return Response(200)


@mod_organization.route('/<organization_slug>/promote/<username>', methods=['POST'])
def promote_member(organization_slug, username):
    org_mongo_utils.promote_member(organization_slug, username)
    return Response(200)


@mod_organization.route('/<organization_slug>/remove/<username>', methods=['POST'])
def remove_member(organization_slug, username):
    org_mongo_utils.remove_member(organization_slug, username)
    return Response(200)


@mod_organization.route('/<organization_slug>/deny/<username>', methods=['POST'])
def deny_member(organization_slug, username):
    org_mongo_utils.deny_member(organization_slug, username)
    return Response(200)


def get_user_name_last_name_by_username(username):
    return user_mongo_utils.get_user_by_username(username)
