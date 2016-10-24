from flask import Blueprint, render_template, url_for, redirect, flash, \
    jsonify, request, Response, current_app, session
from flask.ext.security import login_user, logout_user, current_user, \
    login_required
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed
from app import user_mongo_utils, bcrypt
from slugify import slugify
from bson.objectid import ObjectId

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
                    "organizations": ['kreotive']
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
