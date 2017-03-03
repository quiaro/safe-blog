from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.blog.validation import check_if_post_is_valid
import app.blog.constants as BlogConst


class DeletePost(AuthenticatedHandler):

    @check_if_post_is_valid
    def get(self, post_id=None, post=None):
        self.render('blog/delete-post.html', post=post)

    @check_if_post_is_valid
    def post(self, post_id=None, post=None):
        post.key.delete()
        self.redirect_to(BlogConst.ROUTE_INDEX)
