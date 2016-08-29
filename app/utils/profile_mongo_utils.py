
class ProfileMongoUtils(object):
    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo
        self.collection_name = 'profiles'

    def get_profile(self, slug):
        query = {'slug': slug}
        return self._find_one(query)


    def _find_one(self, query={}, limit=0):

        doc = self.mongo.db[self.collection_name] \
            .find_one(query)

        return doc

    def add_follower(self, followee_slug, follower_slug):

        self.mongo.db[self.collection_name].update(
            {"slug": followee_slug},
            {"$addToSet": {"follower":follower_slug}}
        )

        return True
