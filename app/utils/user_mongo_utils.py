from bson.objectid import ObjectId
import re
from app.mod_profile.mod_views.user import User


class UserMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.users_collection = 'users'
        self.roles_collection = 'roles'
        self.content_collection = 'content'

    def query(self, query):
        """ Make a query by only sending a JSON .
         :param query: JSON object containing the query params
         :rtype: Mongo Cursor
        """
        result = self.mongo.db[self.users_collection] \
            .find(query)
        return result

    def update(self, condition, update_json):
        """ Make a update by only sending a JSON .
         :param query: JSON object containing the update params
         :rtype: Mongo Cursor
        """
        result = self.mongo.db[self.users_collection] \
            .update(condition, {"$set": update_json})
        return result

    def add_user(self, user):
        """ Add user to the database.
         :param user: JSON object containing the user information
         :rtype: Boolean
        """
        user['location'] = ""
        user['mobile'] = ""
        user['telephone'] = ""
        user['about_me'] = ""
        user['role'] = "individual"
        user['avatar_url'] = "img/no-avatar.png"
        user['people_following'] = []
        user['people_followers'] = []
        user['org_following'] = []
        user['username'] = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+ ]", "", user['username']).replace(' ', '').lower()
        self.mongo.db[self.users_collection] \
            .insert(user)
        return True

    def change_avatar(self, username, avatar_url):
        self.mongo.db[self.users_collection] \
            .update({"username": username}, {"$set": {"avatar_url": avatar_url}})
        return True

    def get_role_id(self, name):
        role = self.mongo.db[self.roles_collection] \
            .find_one({"name": name})

        if role != None:
            return ObjectId(role['_id'])
        else:

            # Add role
            self.mongo.db[self.roles_collection] \
                .insert({"name": name, 'description': name})

            # Get role
            role = self.mongo.db[self.roles_collection] \
                .find_one({"name": name})

            return ObjectId(role['_id'])

    def update_user_role(self, username, role_name):
        # Update role for a specific user

        # Get role object
        role = self.get_role_id(role_name)

        # Update mongodb user document with the assigned role
        result = self.mongo.db[self.users_collection] \
            .update({"username": username}, {"$set": {"role": role_name, 'roles': role}})
        return True

    def get_user(self, email):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"email": email})
        if user_cursor is None:
            return None
        else:
            user_instance = User(
                id=unicode(user_cursor['_id']),
                name=user_cursor['name'],
                lastname=user_cursor['lastname'],
                is_active=user_cursor['active'],
                email=user_cursor['email'],
                password=user_cursor['password'],
                roles=user_cursor['roles'],
                role=user_cursor['role'],
                username=user_cursor['username'],
                location=user_cursor['location'],
                telephone=user_cursor['telephone'],
                mobile=user_cursor['mobile'],
                about_me=user_cursor['about_me'],
                avatar_url=user_cursor['avatar_url'],
                people_followers=user_cursor['people_followers'],
                people_following=user_cursor['people_following'],
                org_following=user_cursor['org_following']
            )
            return user_instance

    def get_users(self):
        users = self.mongo.db[self.users_collection] \
            .find()
        return users

    def get_user_by_username(self, username):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"username": username})
        if user_cursor is None:
            return None
        else:
            user_instance = User(
                id=unicode(user_cursor['_id']),
                name=user_cursor['name'],
                lastname=user_cursor['lastname'],
                is_active=user_cursor['active'],
                email=user_cursor['email'],
                password=user_cursor['password'],
                roles=user_cursor['roles'],
                role=user_cursor['role'],
                username=user_cursor['username'],
                location=user_cursor['location'],
                telephone=user_cursor['telephone'],
                mobile=user_cursor['mobile'],
                about_me=user_cursor['about_me'],
                avatar_url=user_cursor['avatar_url'],
                people_followers=user_cursor['people_followers'],
                people_following=user_cursor['people_following'],
                org_following=user_cursor['org_following']
            )
        return user_instance

    def get_user_by_id(self, id):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"_id": ObjectId(id)})
        user_instance = None
        if user_cursor is not None:
            user_instance = User(
                id=unicode(user_cursor['_id']),
                name=user_cursor['name'],
                lastname=user_cursor['lastname'],
                is_active=user_cursor['active'],
                email=user_cursor['email'],
                password=user_cursor['password'],
                roles=user_cursor['roles'],
                role=user_cursor['role'],
                username=user_cursor['username'],
                location=user_cursor['location'],
                telephone=user_cursor['telephone'],
                mobile=user_cursor['mobile'],
                about_me=user_cursor['about_me'],
                avatar_url=user_cursor['avatar_url'],
                people_followers=user_cursor['people_followers'],
                people_following=user_cursor['people_following'],
                org_following=user_cursor['org_following']
            )
        else:
            return None
        return user_instance

    def get_avatar_url(self, username):
        return self.mongo.db[self.users_collection] \
            .find_one({"username": username})['avatar_url']

    def find_user(self, keyword):

        find_user_result = self.mongo.db[self.users_collection] \
            .find({'$text': {'$search': keyword}})

        return find_user_result

    def add_follower(self, follower_username, followee_username, action):
        if action == 'follow':
            added_follower_to_current_user = self.mongo.db[self.users_collection].update(
                {"username": followee_username},
                {"$addToSet": {"people_followers": follower_username}}
            )

            added_followee_to_the_user_ = self.mongo.db[self.users_collection].update(
                {"username": follower_username},
                {"$addToSet": {"people_following": followee_username}}
            )

            if added_followee_to_the_user_['updatedExisting'] and added_follower_to_current_user['updatedExisting']:
                return True
            else:
                return False
        elif action == 'unfollow':

            added_follower_to_current_user = self.mongo.db[self.users_collection].update(
                {"username": followee_username},
                {"$pull": {"people_followers": follower_username}}
            )

            added_followee_to_the_user_ = self.mongo.db[self.users_collection].update(
                {"username": follower_username},
                {"$pull": {"people_following": followee_username}}
            )

            if added_followee_to_the_user_['updatedExisting'] and added_follower_to_current_user['updatedExisting']:
                return True
            else:
                return False

    def delete_user(self, username):
        """ Delete user from the database.
        :rtype: MongoDB Cursor with all the users
        """
        delete_user = self.mongo.db[self.users_collection] \
            .remove({"username": username})

        delete_users_content = self.mongo.db[self.content_collection] \
            .remove({"author.slug": username})

        return delete_user and delete_users_content

    def change_pass(self, username, new_password):
        from app import bcrypt
        new_pass = self.mongo.db[self.users_collection] \
            .update({"username": username},
                    {"$set": {"password": bcrypt.generate_password_hash(new_password, rounds=12)}})

        return new_pass
