from app.models.blogpost import BlogPost
from app.authenticated_handler import AuthenticatedHandler


class EditPost(AuthenticatedHandler):

    def get(self, post_id=None):
        post = BlogPost.get_by_id(int(post_id), parent=self.user.key)
        if post:
            self.render_internal('blog/update-post.html',
                                  post=post,
                                  is_editing=True,
                                  home=self.uri_for(Blog.routes.get('show_post'), post_id=post.key.id()))
        else:
            self.error(404)
            return

    def post(self, post_id=None):
        post = BlogPost.get_by_id(int(post_id), parent=self.user.key)

        if post:
            post.subject = self.request.get('subject')
            post.content = self.request.get('content')

            if post.subject and post.content:
                post.put()
                self.redirect_to(Blog.routes.get('show_post'), post_id=post.key.id())
            else:
                error = "Subject and content fields are required."
                self.render("blog/update-post.html",
                            post=post,
                            is_editing=True,
                            error=error,
                            home=self.uri_for(Blog.routes.get('show_post'), post_id=post.key.id()))
        else:
            self.error(404)
            return
