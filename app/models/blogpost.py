from google.appengine.ext import ndb
from string import find

from app.utils.template_renderer import TemplateRenderer


def get_blog_group(group='default'):
    return ndb.Key('Group', group)


class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.KeyProperty(kind='User', required=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def create(cls, subject, content, owner, group='default'):
        return cls(parent=get_blog_group(group),
                   subject=subject,
                   content=content,
                   owner=owner)

    @classmethod
    def by_id(cls, post_id, group='default'):
        return cls.get_by_id(int(post_id), parent=get_blog_group(group))

    @classmethod
    def created_by(cls, user, group='default'):
        return cls.query(ancestor=get_blog_group(group)).filter(BlogPost.owner == user.key).fetch()

    @classmethod
    def not_created_by(cls, user, group='default'):
        return cls.query(ancestor=get_blog_group(group)).filter(BlogPost.owner != user.key).fetch()

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return TemplateRenderer.render('blog/post.html', p=self)

    def render_teaser(self):
        # truncate content to show only the first paragraph of the post
        # (marked by 2 consecutive newline characters)
        end_of_first_paragraph = find(self.content, '\r\n\r\n')
        if (end_of_first_paragraph == -1):
            end_of_first_paragraph = len(self.content)
        self._render_text = self.content[0:end_of_first_paragraph].replace('\n', '<br>')
        return TemplateRenderer.render('blog/teaser.html', p=self)
