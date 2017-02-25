from google.appengine.ext import ndb

from app.utils.template_renderer import TemplateRenderer

class Comment(ndb.Model):
    user = ndb.UserProperty(indexed=False, required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    created_by = ndb.KeyProperty(required = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    def __init__(self, *args, **kwds):
        super(BlogPost, self).__init__(*args, **kwds)
        self.t_renderer = TemplateRenderer()

    @classmethod
    def created_by(cls, user):
        return cls.query(ancestor=user.key).order(cls.created).fetch()

    @classmethod
    def not_created_by(cls, user):
        return cls.query().filter(ndb.GenericProperty("created_by") != user.key).fetch()

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return self.t_renderer.render("blog/post.html", p = self)
