from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost


class DeletePost(AuthenticatedHandler):

    def get(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return
        if post.owner != self.user.key:
            self.error(403)
            return

        self.render_internal('blog/delete-post.html',
                             post=post,
                             edit_post=self.uri_for('blog_edit_post', post_id=post.key.id()))

    def post(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return
        if post.owner != self.user.key:
            self.error(403)
            return

        post.key.delete()
        self.redirect_to('blog_index')
