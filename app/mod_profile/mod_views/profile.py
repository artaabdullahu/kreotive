from flask import render_template, request, Response, redirect, url_for, send_from_directory
from flask.ext.security import current_user, login_required
from app import profile_mongo_utils, content_mongo_utils,org_mongo_utils, user_mongo_utils, allowed_extensions, upload_folder, bcrypt
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from datetime import datetime
import app

UPLOAD_FOLDER = 'app/static/uploads/'

class Profile():

    def archive(self, username):
        ''' Loads the article archive page.
        '''
        # get the profile object for the given username
        profile = user_mongo_utils.get_user_by_username(username)
        category = content_mongo_utils.get_categories()
        articles_by_category = content_mongo_utils.count_articles_by_category(profile.username, category)
        return render_template('mod_profile/archive.html', profile=profile, articles_by_category=articles_by_category)

    def search(self, username):
        ''' Loads the article archive page.
        '''
        # get the profile object for the given username
        profile = user_mongo_utils.get_user_by_username(username)
        feed = content_mongo_utils.get_authors_articles(profile.username)
        return render_template('mod_profile/search.html', profile=profile, feed=feed)

    def about(self, username):
        ''' Loads the about page.
        '''
        # get the profile object for the given username
        profile = user_mongo_utils.get_user_by_username(username)
        articles_no = content_mongo_utils.count_articles(username)
        followers_no = profile_mongo_utils.count_followers(username)

        return render_template('mod_profile/about.html', profile=profile, articles_no = articles_no, followers_no=followers_no)

    def feed(self, username):
        ''' Loads the feed page.
        '''
        if current_user.is_authenticated:
            # get the profile object for the given username
            profile = user_mongo_utils.get_user_by_username(username)
            feed = dumps(content_mongo_utils.get_authors_paginated_articles(profile.username, 0, 8))
        else:
            feed = None
            profile = current_user
        return render_template('mod_profile/feed.html', profile=profile, feed=feed)

    def category_feed(self, username, category):
        ''' Loads the feed page with specific category article.
                '''
        # get the profile object for the given username
        profile = user_mongo_utils.get_user_by_username(username)
        feed = dumps(content_mongo_utils.get_articles_one_category_only(profile.username, category))
        return render_template('mod_profile/feed.html', profile=profile, feed=feed)


    def follow(self, username, action):
        '''
        TODO:
            1. Get POST reuqest body JSON
            2. Get the username of the follower.
            3. Implement profile_mongo_utils.add_follower()
            4. Call profile_mongo_utils.add_follower()
            5. Check if it adds the follower username in the document.
            6. Implement profile_mongo_utils.remove_follower()
        '''
        followee_username = current_user.username
        user_mongo_utils.add_follower(followee_username, username, action)

        resp = Response(status=200)
        return resp

    def paginated_author_articles(self, username, skip_posts_number, posts_per_page):
        # TODO: Restrict access to only authenticated users
        # get the profile object for the given username
        profile = user_mongo_utils.get_user_by_username(username)
        articles = dumps(
            content_mongo_utils.get_authors_paginated_articles(profile.id, skip_posts_number, posts_per_page))
        return Response(response=articles)

    @login_required
    def profile_settings(self, username):
        # Get the profile info
        error = ""
        if request.method == "GET":
            profile = user_mongo_utils.get_user_by_username(username)
            return render_template('mod_profile/account.html', profile=profile, error=error)
        elif request.method == "POST":
            error = "SSSS"
            profile = user_mongo_utils.get_user_by_username(username)
            user_json = {}
            if request.form['email'] is not None:
                user_json['email'] = request.form['email']
                user_json['name'] = request.form['name']
                user_json['location'] = request.form['location']
                user_json['telephone'] = request.form['telephone']
                user_json['mobile'] = request.form['mobile']
                user_json['about_me'] = request.form['about_me']
                user_mongo_utils.update({'username': current_user.username},user_json )
                error = "Succesfully updated profile."
            return redirect(url_for('profile.profile_settings', username=username, error=error))

    def articles(self, username):
        return render_template('mod_profile/articles.html')

    @login_required
    def following(self, username):
        # get the profile object for the given username
        profile = user_mongo_utils.get_user_by_username(username)
        organization = org_mongo_utils.get_organizations()
        return render_template('mod_profile/following.html', profile=profile, organization=organization)

    @login_required
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in allowed_extensions

    @login_required
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
                photo_url = 'uploads/' + str(current_user.username) + '/' + str(datetime.now().strftime('%Y-%m')) + "/" + filename
                user_mongo_utils.change_avatar(current_user.username, photo_url)
                return redirect(url_for('profile.profile_settings',
                                        username=current_user.username))
        return redirect(url_for('profile.profile_settings', username=current_user.username, error=error))

    @login_required
    def get_avatar_url(self, username):
        user  = user_mongo_utils.get_user_by_username(username)
        return user['avatar_url']


    @login_required
    def delete_profile(self, username):
        user = user_mongo_utils.delete_user(username)
        return redirect(url_for('main.feed'))

    @login_required
    def change_password(self,username):
        profile = user_mongo_utils.get_user_by_username(username)
        email = current_user.email
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        user_input = user_mongo_utils.get_user(email=email)
        password_check = bcrypt.check_password_hash(user_input.password, old_password)
        if password_check:
            if new_password == confirm_new_password:
                user_mongo_utils.change_pass(username, new_password)
                return render_template('mod_profile/account.html', profile=profile, success="Password was changed successfully")
            else:
                return render_template('mod_profile/account.html', profile=profile, error="Passwords didn't match")
        else:
                return render_template('mod_profile/account.html', profile=profile, error="This isn't your actual password")


def user_avatar(username):
    avatar_url  = user_mongo_utils.get_user_by_username(username)['avatar_url']
    return avatar_url
