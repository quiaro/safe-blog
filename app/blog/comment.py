from google.appengine.ext import ndb

from app.authenticated_handler import AuthenticatedHandler
from app.blog.validation import check_if_comment_is_valid
import app.blog.constants as BlogConst


class Comment(AuthenticatedHandler):

    @check_if_comment_is_valid
    def update(self, comment_str=None, comment=None):
        comment_body = self.request.get('comment')
        post_id = comment.get_post_id()

        # The comment cannot be blank. If it is, then ignore the update.
        if comment_body:
            comment.content = comment_body
            comment.put()

        # Back to viewing the post
        self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=post_id)

    @check_if_comment_is_valid
    def delete(self, comment_str=None, comment=None):
        post_id = comment.get_post_id()
        comment.key.delete()

        # Back to viewing the post
        self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=post_id)
