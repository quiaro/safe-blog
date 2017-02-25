from google.appengine.ext import ndb

from app.utils.template_renderer import TemplateRenderer
from app.models.user import User


class Comment(ndb.Model):
    user = ndb.UserProperty(indexed=False, required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    owner = ndb.KeyProperty(kind=User)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    @classmethod
    def created_by(cls, user):
        return cls.query(ancestor=user.key).order(cls.created).fetch()

    @classmethod
    def not_created_by(cls, user):
        return cls.query().filter(BlogPost.owner != user.key).fetch()

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return TemplateRenderer.render("blog/post.html", p = self)
