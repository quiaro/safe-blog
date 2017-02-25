from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost


class EditPost(AuthenticatedHandler):

    def get(self, post_id=None):
        post = BlogPost.get_by_id(int(post_id), parent=self.user.key)
        if post:
            post_id = post.key.id()
            self.render_internal('blog/update-post.html',
                                  post=post,
                                  is_editing=True,
                                  delete_post=self.uri_for(Blog.routes.get('delete_post'), post_id=post_id),
                                  home=self.uri_for(Blog.routes.get('show_post'), post_id=post_id))
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
                post_id = post.key.id()
                error = "Subject and content fields are required."
                self.render("blog/update-post.html",
                            post=post,
                            is_editing=True,
                            error=error,
                            delete_post=self.uri_for(Blog.routes.get('delete_post'), post_id=post_id),
                            home=self.uri_for(Blog.routes.get('show_post'), post_id=post_id))
        else:
            self.error(404)
            return
