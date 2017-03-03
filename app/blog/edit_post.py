from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.blog.validation import check_if_post_is_valid
import app.blog.constants as BlogConst


class EditPost(AuthenticatedHandler):

    @check_if_post_is_valid
    def get(self, post_id=None, post=None):
        self.render('blog/update-post.html',
                      post=post,
                      is_editing=True)

    @check_if_post_is_valid
    def post(self, post_id=None, post=None):
        post.subject = self.request.get('subject')
        post.content = self.request.get('content')

        if post.subject and post.content:
            post.put()
            self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=post.key.id())
        else:
            post_id = post.key.id()
            error = "Subject and content fields are required."
            self.render("blog/update-post.html",
                        post=post,
                        is_editing=True,
                        error=error)
