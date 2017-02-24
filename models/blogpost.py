from google.appengine.ext import ndb

class Comment(nbd.Model):
    user = ndb.UserProperty(indexed=False, required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True, default='')
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
