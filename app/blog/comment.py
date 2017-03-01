import webapp2

from app.models.blogpost import BlogPost
from app.blog.view_post import ViewPost


class Comment(ViewPost):

    def update(self, post_id=None, comment_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        self.write('Update comment!')

    def delete(self, post_id=None, comment_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        self.write('Delete comment!')
