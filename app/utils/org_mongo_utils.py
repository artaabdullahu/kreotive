import pprint


class OrgMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.org_collection = 'organizations'
        self.users_collection = 'users'

    def add_org(self, org):
        """ Add user to the database.
         :param org: JSON object containing the user information
         :rtype: Boolean
        """
        self.mongo.db[self.org_collection] \
            .insert(org)
        return True

    def update_org(self, condition, update_json):
        """ Make a update by only sending a JSON .
         :param query: JSON object containing the update params
         :rtype: Mongo Cursor
        """
        result = self.mongo.db[self.org_collection] \
            .update(condition, {"$set": update_json})
        return result


    def get_org_by_slug(self, org_slug):
        """ Get an organization by slug.
         :param org_slug: Slug of the organization
         :rtype: MongoDB Cursor
        """
        org_cursor = self.mongo.db[self.org_collection] \
            .find_one({"org_slug": org_slug})
        return org_cursor

    def get_organizations(self):
        """ Get all organizations.
         :rtype: MongoDB Cursor
        """
        org_cursor = self.mongo.db[self.org_collection] \
            .find().sort([("_id", -1)])
        return org_cursor

    def find_org(self, keyword):

        find_org_result = self.mongo.db[self.org_collection] \
            .find({'$text': {'$search': keyword}})
        return find_org_result

    def add_follower(self, follower_username, organization_slug, action):
        if action == 'follow':
            added_follower_to_current_user = self.mongo.db[self.org_collection].update(
                {"org_slug": organization_slug},
                {"$addToSet": {"followers": follower_username}}
            )

            added_followee_to_the_user_ = self.mongo.db[self.users_collection].update(
                {"username": follower_username},
                {"$addToSet": {"org_following": organization_slug}}
            )

            if added_followee_to_the_user_['updatedExisting'] and added_follower_to_current_user['updatedExisting']:
                return True
            else:
                return False
        elif action == 'unfollow':

            added_follower_to_current_user = self.mongo.db[self.org_collection].update(
                {"org_slug": organization_slug},
                {"$pull": {"followers": follower_username}}
            )

            added_followee_to_the_user_ = self.mongo.db[self.users_collection].update(
                {"username": follower_username},
                {"$pull": {"org_following": organization_slug}}
            )

            if added_followee_to_the_user_['updatedExisting'] and added_follower_to_current_user['updatedExisting']:
                return True
            else:
                return False

    def find_org_by_admin(self, username):
        find_org_result = self.mongo.db[self.org_collection] \
            .find_one({'org_admin':{"$in":[username]}})
        return find_org_result

    # Membership administration

    def ask_to_join(self, username, organization_slug):
        """ Ask to join to an organization
         :param :
         :rtype:
        """

        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug},
            {"$addToSet": {"members": {"username": username, "status": 'pending'}}}
        )
        return True

    def accept_member(self, organization_slug, username):
        """ Get an organization by slug.
         :param :
         :rtype:
        """
        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug, 'members.username': username},
            {"$set": {"members.$.status": 'member'}}
        )
        return True

    def remove_member(self, organization_slug, username):
        """ Remove member
         :param :
         :rtype:
        """
        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug},
            {"$pull": {"members": {'username': username}}}
        )
        return True

    def denote_member(self, organization_slug, username):
        """ Denote member
         :param :
         :rtype:
        """
        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug, 'members.username': username},
            {"$set": {"members.$.status": 'member'}}
        )
        return True

    def promote_member(self, organization_slug, username):
        """ Promote member
         :param :
         :rtype:
        """
        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug, 'members.username': username},
            {"$set": {"members.$.status": 'editor'}}
        )
        return True

    def promote_member_to_admin(self, organization_slug, username):
        """ Promote member to admin
         :param :
         :rtype:
        """
        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug, 'members.username': username},
            {"$set": {"members.$.status": 'member'}}
        )
        return True

    def deny_member(self, organization_slug, username):
        """ Promote member to admin
         :param :
         :rtype:
        """
        self.mongo.db[self.org_collection].update(
            {"org_slug": organization_slug, 'members.username': username},
            {"$set": {"members.$.status": 'denied'}}
        )
        return True

    def get_users_by_status(self, organization_slug, status):

        result = self.mongo.db[self.org_collection].find_one({'org_slug': organization_slug},
                                                    {'members': {"$elemMatch": {'status': status}}})
        return result


    def check_if_user_is_member_of(self, organization_slug, username):

        result = self.mongo.db[self.org_collection].find_one({'org_slug': organization_slug},
                                                             {'members': {"$elemMatch": {'username': username}}})

        return result
