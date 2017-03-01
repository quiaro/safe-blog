from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost
import app.blog.constants as BlogConst


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
                             edit_post=self.uri_for(BlogConst.ROUTE_EDIT_POST, post_id=post.key.id()))

    def post(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return
        if post.owner != self.user.key:
            self.error(403)
            return

        post.key.delete()
        self.redirect_to(BlogConst.ROUTE_INDEX)
