from flask import Blueprint, render_template
from app import user_mongo_utils, bcrypt, org_mongo_utils
from flask import request
from flask import Response
import json
from slugify import slugify
from bson.objectid import ObjectId

mod_superadmin = Blueprint('superadmin', __name__, url_prefix='/sadmin')


@mod_superadmin.route('/', methods=['GET'])
def index():
    return render_template('mod_superadmin/index.html')


@mod_superadmin.route('/users', methods=['GET'])
def users():
    users = user_mongo_utils.get_users()
    return render_template('mod_superadmin/users.html', users=users)


@mod_superadmin.route('/users/add', methods=['GET', 'POST'])
def add_users():
    error = ""
    if request.method == 'GET':
        return render_template('mod_superadmin/add_users.html')
    elif request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        user_check = user_mongo_utils.get_user(email=email)
        if user_check:
            error = "A user with that e-mail already exists in the database"
            return render_template('mod_superadmin/add_users.html', error=error)
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
                    "roles": [user_mongo_utils.get_role_id(role)],
                    "organizations": ['kreotive']
                }
                # TODO: Regiser user
                user_mongo_utils.add_user(user_json)
                error = "User registered, if you want to continue adding users, fill the form and click Add User"
                return render_template('mod_superadmin/add_users.html', error=error)
            else:
                error = "Password error."
                return render_template('mod_superadmin/add_users.html', error=error)


@mod_superadmin.route('/organizations', methods=['GET'])
def organizations():
    organizations = org_mongo_utils.get_organizations()
    return render_template('mod_superadmin/organizations.html', organizations=organizations)


@mod_superadmin.route('/organizations/add', methods=['GET', 'POST'])
def add_org():
    if request.method == 'GET':
        users = user_mongo_utils.get_users()
        users_list = []
        for user in users:
            users_list.append(user['username'])
        return render_template('mod_superadmin/add_org.html', users_list=users_list, get_user_name_last_name_by_username=get_user_name_last_name_by_username)
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        location = request.form['location']
        telephone = request.form['telephone']
        mobile = request.form['mobile']
        about_org = request.form['about_org']
        admin = request.form['org_admin']

        user_mongo_utils.update_user_role(admin, 'org_admin')

        org_slug = slugify(name) + '-' + str(ObjectId())

        if org_mongo_utils.get_org_by_slug({"slug": org_slug}):
            error = "Organization exists"
            return render_template('mod_superadmin/add_org.html', error=error)
        else:

            org_json = {
                "name": name,
                "email": email,
                "active": True,
                "org_slug": org_slug,
                "org_admin": [slugify(admin)],
                "followers": [],
                "location": location,
                "telephone": telephone,
                "mobile": mobile,
                "about_org":about_org,

            }

        org_mongo_utils.add_org(org_json)

        error = "Organization is registered, if you want to continue adding organizations, fill the form and click Add Organization"
        users = user_mongo_utils.get_users()
        users_list = []
        for user in users:
            users_list.append(user['username'])
        return render_template('mod_superadmin/add_org.html', error=error, users_list=users_list, get_user_name_last_name_by_username=get_user_name_last_name_by_username)

def get_user_name_last_name_by_username(username):
    return user_mongo_utils.get_user_by_username(username)

