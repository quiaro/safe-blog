from app.models.blogpost import BlogPost
from app.models.comment import Comment

def check_if_post_exists(handler):
    def decorated_handler(self, post_id):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        handler(self, post_id, post)
    return decorated_handler

def check_if_post_is_valid(handler):
    def decorated_handler(self, post_id):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        if post.owner != self.user.key:
            self.error(403)
            return

        handler(self, post_id, post)
    return decorated_handler

def check_if_comment_is_valid(handler):
    def decorated_handler(self, comment_str):
        comment = Comment.by_string(comment_str)

        if not comment:
            self.error(404)
            return

        if comment.user != self.user.key:
            self.error(403)
            return

        handler(self, comment_str, comment)
    return decorated_handler
