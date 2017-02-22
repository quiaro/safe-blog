from google.appengine.ext import ndb

class User(ndb.Model):
    pass

    @classmethod
    def by_name(cls, name):
        # TODO: Implement
        return False

    @classmethod
    def register(cls, name, pw_hash, email = None):
        # TODO: Implement
        return None
