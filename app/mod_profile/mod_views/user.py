# coding=utf-8
from flask import redirect, url_for
from flask.ext.security import UserMixin, RoleMixin
import datetime
from werkzeug.security import check_password_hash


class User(UserMixin):
    def __init__(self, id=None, name=None, lastname=None, is_active=None, email=None, password=None, roles=None,
                 role=None, username=None, location=None, telephone=None, mobile=None, about_me=None, avatar_url=None,
                 people_following=None, people_followers=None, org_following=None, organization=None):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.roles = [Roles(role, role, 'description')]
        self.role = role
        self.confirmed_at = datetime.datetime.now()
        self.username = username
        self.location = location
        self.telephone = telephone
        self.mobile = mobile
        self.about_me = about_me
        self.avatar_url = avatar_url
        self.active = is_active
        self.people_following = people_following
        self.people_followers = people_followers
        self.org_following = org_following
        self.organization = organization

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


class Roles(RoleMixin):
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def get_role(self):
        return ''


class UserDataStore(object):
    @staticmethod
    def activate_user(self, user):
        """
        Activates a specified user. Returns True if a change was made.
        Parameters: user – The user to activate
        :param user:
        :return:
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def find_user(id):
        from app import user_mongo_utils
        user = user_mongo_utils.get_user_by_id(id)
        return user

    @staticmethod
    def add_role_to_user(self, user, role):
        """
        :param user: The user to manipulate
        :param role: The role to add to the user
        :return:Adds a role to a user.
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def create_role(self, **kwargs):
        """
        Creates and returns a new role from the given parameters.
        :param kwargs:
        :return:
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def create_user(self, **kwargs):
        """
        Creates and returns a new user from the given parameters.
        :param kwargs:
        :return:
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def deactivate_user(self, user):
        """
         Deactivates a specified user. Returns True if a change was made.
        :param user:  The user to deactivate
        :return: Deactivates the specified user.
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def delete_user(self, id):
        """
        Deletes the specified user.
        :param user: The user to delete
        :return: True if the user is deleted.
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def find_or_create_role(self, name, **kwargs):
        """
        Returns a role matching the given name or creates it with any additionally provided parameters.
        :param name:
        :param kwargs:
        :return:
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def remove_role_from_user(self, user, role):
        """
        Removes a role from a user.
        :param user: The user to manipulate
        :param role:  The role to remove from the user
        :return:
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def toggle_active(self, user):
        """
         Toggles a user’s active status. Always returns True.
        :param user:
        :return:
        """
        # TODO : Implement this method
        return True

    @staticmethod
    def is_a_member_of(self, user, organization):
        """
         Returns True if user is a member of the organization
        :param user:
        :return:
        """
        # TODO : Implement this method
        from app import org_mongo_utils

        is_member =  org_mongo_utils.check_if_user_is_member_of(user, organization)
        return is_member