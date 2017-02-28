import random
import hashlib
from string import letters
from google.appengine.ext import ndb


def make_salt(length=8):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def get_user_group(group = 'default'):
    return ndb.Key('Group', group)


class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(indexed=False, required=True)
    email = ndb.StringProperty(indexed=False)
    favorite_posts = ndb.KeyProperty(kind="BlogPost", repeated=True)

    def likes(self, post):
        return post.key in self.favorite_posts

    def add_favorite(self, post):
        return self.favorite_posts.append(post.key)

    def remove_favorite(self, post):
        if post.key in self.favorite_posts:
            return self.favorite_posts.remove(post.key)

    @classmethod
    def by_username(cls, username, group='default'):
        return cls.get_by_id(username, parent=get_user_group(group))

    @classmethod
    def register(cls, username, pw, email=None, group='default'):
        pw_hash = make_pw_hash(username, pw)
        return cls(id=username,
                   parent=get_user_group(group),
                   username=username,
                   pw_hash=pw_hash,
                   email=email)

    @classmethod
    def authenticate(cls, username, pw):
        u = cls.by_username(username)
        if u and valid_pw(username, pw, u.pw_hash):
            return u
