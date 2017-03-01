from google.appengine.ext import ndb

from app.authenticated_handler import AuthenticatedHandler
from app.models.comment import Comment as CommentModel
import app.blog.constants as BlogConst


class Comment(AuthenticatedHandler):

    def update(self, comment_str=None):
        comment = CommentModel.by_string(comment_str)

        if not comment:
            self.error(404)
            return

        if comment.user != self.user.key:
            self.error(403)
            return

        comment_body = self.request.get('comment')
        post_id = comment.get_post_id()

        # The comment cannot be blank. If it is, then ignore the update.
        if comment_body:
            comment.content = comment_body
            comment.put()

        # Back to viewing the post
        self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=post_id)

    def delete(self, comment_str=None):
        comment = CommentModel.by_string(comment_str)

        if not comment:
            self.error(404)
            return

        if comment.user != self.user.key:
            self.error(403)
            return

        post_id = comment.get_post_id()
        comment.key.delete()

        # Back to viewing the post
        self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=post_id)
