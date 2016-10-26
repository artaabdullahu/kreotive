from flask import Blueprint, render_template, url_for, redirect, flash, \
    jsonify, request, Response, current_app, session
from flask.ext.security import login_user, logout_user, current_user, \
    login_required
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed
from app import user_mongo_utils, bcrypt, facebook, google
from slugify import slugify
from bson.objectid import ObjectId
import json
import random

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template('mod_auth/sign_up.html')
    elif request.method == "POST":
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form['confirm_password']

        user_check = user_mongo_utils.get_user(email=email)
        if user_check:
            error = "A user with that e-mail already exists in the database"
            return render_template('mod_auth/sign_up.html', error=error)
        else:
            if password == confirm_password:
                user_json = {
                    "name": name,
                    "lastname": lastname,
                    "email": email,
                    "username": name + lastname + '-' + str(ObjectId()),
                    "password": bcrypt.generate_password_hash(password, rounds=12),
                    "active": True,
                    "user_slug": slugify(name + ' ' + lastname),
                    "roles": [user_mongo_utils.get_role_id('individual')],
                    "organizations": []
                }
                # Regiser user
                user_mongo_utils.add_user(user_json)

                #  login user
                user_data = user_mongo_utils.get_user(email=email)
                login_user(user_data)

                return redirect(url_for('profile.profile_settings', username=user_data.username))
            else:
                error = "Passowrds didn't match"
                return render_template('mod_auth/sign_up.html', error=error)


@mod_auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('main.feed'))
        else:
            return render_template('mod_auth/log_in.html')
    elif request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user_input = user_mongo_utils.get_user(email=email)
        if user_input is None:
            error = 'Please write both username and password', 'error'
            return render_template('mod_auth/log_in.html', error=error)
        elif user_input != None:
            password_check = bcrypt.check_password_hash(user_input.password, password)
            email_check = True if user_input.email == email else False
            if not email_check:
                error = 'Wrong email'
                return render_template('mod_auth/log_in.html', error=error)
            elif not password_check:
                error = 'Wrong password'
                return render_template('mod_auth/log_in.html', error=error)
            elif password_check and email_check:
                login_user(user_input)
                # Tell Flask-Principal the identity changed
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(current_user.id))
                return redirect(url_for('main.feed'))


@login_required
@mod_auth.route('/logout')
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('main.feed'))


@mod_auth.route('/facebook/login')
def fb_login():
    redirect_uri = url_for('auth.fb_authorized', _external=True)
    params = {'redirect_uri': redirect_uri, 'response_type': 'code'}
    return redirect(facebook.get_authorize_url( **params))


@mod_auth.route('/facebook/authorized')
def fb_authorized():
    # check to make sure the user authorized the request
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('auth.login'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('auth.fb_authorized', _external=True)
    data = {'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri}
    # authorize_url = facebook.get_authorize_url(request_token)
    session = facebook.get_auth_session(data=data)
    # session = OAuth2Session(facebook.client_id, facebook.client_secret, access_token=data['code'])
    # the "me" response
    me = session.get('/me?locale=en_US&fields=first_name,last_name,email,about,picture').json()
    first_name = me['first_name']
    last_name = me['last_name']

    password = ''.join(random.choice('abcdefghij') for _ in range(10))
    id =  me['id']
    user_json = {
        "facebook_id":id,
        "name": first_name,
        "lastname": last_name ,
        "email": '',
        "username": first_name + last_name + '-' + str(ObjectId()),
        "password": bcrypt.generate_password_hash(password, rounds=12),
        "active": True,
        "user_slug": slugify(first_name + ' ' + last_name),
        "roles": [user_mongo_utils.get_role_id('individual')],
        "organizations": []
    }
    user = user_mongo_utils.get_user_by_facebook_id(id)
    if user == None:
        # Regiser user
        user_mongo_utils.add_user(user_json)
        user = user_mongo_utils.get_user_by_facebook_id(id)
        #  login user
        login_user(user)
    else:
        login_user(user)

    return redirect(url_for('profile.profile_settings', username=user.username))

@mod_auth.route('/google/login')
def google_login():
    redirect_uri = url_for('auth.google_authorized', _external=True)
    params = {'redirect_uri': redirect_uri, 'response_type': 'code'}
    return redirect(google.get_authorize_url( **params))

@mod_auth.route('/google/authorized')
def google_authorized():
    # check to make sure the user authorized the request
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('auth.login'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('auth.google_authorized', _external=True)
    data = {'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri}
    session = google.get_auth_session(data=data)

    me = session.get('/me?locale=en_US&fields=first_name,last_name,email,about,picture').json()
    first_name = me['given_name']
    last_name = me['family_name']

    password = ''.join(random.choice('abcdefghij') for _ in range(10))
    id =  me['id']
    user_json = {
        "facebook_id":id,
        "name": first_name,
        "lastname": last_name ,
        "email": '',
        "username": first_name + last_name + '-' + str(ObjectId()),
        "password": bcrypt.generate_password_hash(password, rounds=12),
        "active": True,
        "user_slug": slugify(first_name + ' ' + last_name),
        "roles": [user_mongo_utils.get_role_id('individual')],
        "organizations": []
    }
    user = user_mongo_utils.get_user_by_facebook_id(id)
    if user == None:
        # Regiser user
        user_mongo_utils.add_user(user_json)
        user = user_mongo_utils.get_user_by_facebook_id(id)
        #  login user
        login_user(user)
    else:
        login_user(user)

    return redirect(url_for('profile.profile_settings', username=user.username))

