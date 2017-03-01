from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost
import app.blog.constants as BlogConst


class NewPost(AuthenticatedHandler):

    def get(self):
        post = {}
        self.render_internal('blog/update-post.html',
                             post=post,
                             is_editing=False,
                             home=self.uri_for(BlogConst.ROUTE_INDEX))

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = BlogPost.create(subject, content, self.user.key)
            p.put()
            self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=p.key.id())
        else:
            error = "Subject and content fields are required."
            post = {
                subject: subject,
                content: content
            }
            self.render("blog/update-post.html",
                        post=post,
                        is_editing=False,
                        error=error,
                        home=self.uri_for(BlogConst.ROUTE_INDEX))
