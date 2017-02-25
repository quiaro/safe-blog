from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost


class NewPost(AuthenticatedHandler):

    def get(self):
        post = {}
        self.render_internal('blog/update-post.html',
                             post=post,
                             is_editing=False,
                             home=self.uri_for(Blog.routes.get('index')))

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = BlogPost(parent=self.user.key,
                         subject=subject,
                         content=content,
                         owner=self.user.key)
            p.put()
            self.redirect_to(Blog.routes.get('show_post'), post_id=p.key.id())
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
                        home=self.uri_for(Blog.routes.get('index')))
