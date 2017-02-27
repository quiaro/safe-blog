from google.appengine.ext import ndb
from string import find

from app.utils.template_renderer import TemplateRenderer
from app.models.user import User

def get_blog_group(group = 'default'):
    return ndb.Key('Group', group)


class Comment(ndb.Model):
    user = ndb.UserProperty(indexed=False, required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    owner = ndb.KeyProperty(kind=User, required=True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    @classmethod
    def create(cls, subject, content, owner, group='default'):
        return cls(parent=get_blog_group(group),
                   subject=subject,
                   content=content,
                   owner=owner)

    @classmethod
    def by_id(cls, post_id, group='default'):
        return cls.get_by_id(post_id, parent=get_blog_group(group))

    @classmethod
    def created_by(cls, user):
        return cls.query().filter(BlogPost.owner == user.key).fetch()

    @classmethod
    def not_created_by(cls, user):
        return cls.query().filter(BlogPost.owner != user.key).fetch()

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return TemplateRenderer.render("blog/post.html", p = self)

    def render_teaser(self, post_link):
        # truncate content to show only the first paragraph of the post
        # (marked by 2 consecutive newline characters)
        end_of_first_paragraph = find(self.content, "\r\n\r\n")
        if (end_of_first_paragraph == -1):
            end_of_first_paragraph = len(self.content)
        self._render_text = self.content[0:end_of_first_paragraph].replace('\n', '<br>')
        return TemplateRenderer.render("blog/teaser.html", p = self, post_link=post_link)
