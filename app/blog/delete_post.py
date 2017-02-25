from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost


class DeletePost(AuthenticatedHandler):

    def get(self, post_id=None):
        post = BlogPost.get_by_id(int(post_id), parent=self.user.key)
        if post:
            self.render_internal('blog/delete-post.html',
                                 post=post,
                                 edit_post=self.uri_for(Blog.routes.get('edit_post'), post_id=post.key.id()))
        else:
            self.error(404)
            return

    def post(self, post_id=None):
        post = BlogPost.get_by_id(int(post_id), parent=self.user.key)
        if post:
            post.key.delete()
            self.redirect_to(Blog.routes.get('index'))
        else:
            self.error(404)
            return
