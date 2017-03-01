from google.appengine.ext import ndb

from app.utils.template_renderer import TemplateRenderer

class Comment(ndb.Model):
    user = ndb.KeyProperty(kind='User', required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_post(cls, post):
        return cls.query(ancestor=post.key).fetch()

    def render(self, user):
        if self.user == user.key:
            self._username = 'you'
            template = 'blog/comment-by-owner.html'
        else:
            self._username = self.user.get().username
            template = 'blog/comment.html'
        self._render_text = self.content.replace('\n', '<br>')
        return TemplateRenderer.render(template, c=self)
