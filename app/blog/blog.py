import webapp2

from app.models.blogpost import BlogPost
from app.authenticated_handler import AuthenticatedHandler


class Blog(AuthenticatedHandler):

    routes = dict(
        index='blog',
        new_post='new_post',
        edit_post='edit_post',
        delete_post='delete_post',
        show_post='show_post',
        modify_post='modify_post',
    )

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/blog',
                          handler=Blog,
                          handler_method='home',
                          methods=['GET'],
                          name=Blog.routes.get('index')),

            webapp2.Route(r'/blog/new-post',
                          handler='app.blog.new_post.NewPost',
                          name=Blog.routes.get('new_post')),

            webapp2.Route(r'/blog/<post_id>/edit',
                          handler='app.blog.edit_post.EditPost',
                          name=Blog.routes.get('edit_post')),

            webapp2.Route(r'/blog/<post_id>/delete',
                          handler='app.blog.delete_post.DeletePost',
                          name=Blog.routes.get('delete_post')),

            webapp2.Route(r'/blog/<post_id>',
                          handler=Blog,
                          handler_method='show_post',
                          methods=['GET'],
                          name=Blog.routes.get('show_post')),

            webapp2.Route(r'/blog/<post_id>',
                          handler=Blog,
                          handler_method='modify_post',
                          methods=['POST'],
                          name=Blog.routes.get('modify_post')),
        ]

    def home(self):
        my_posts = BlogPost.created_by(self.user)
        other_posts = BlogPost.not_created_by(self.user)
        edit_post_fn = lambda p: self.uri_for(Blog.routes.get('edit_post'), post_id=p.key.id())
        view_post_fn = lambda p: self.uri_for(Blog.routes.get('show_post'), post_id=p.key.id())
        self.render_internal('blog/home.html',
                              my_posts=my_posts,
                              other_posts=other_posts,
                              edit_post_fn=edit_post_fn,
                              view_post_fn=view_post_fn,
                              new_post=self.uri_for(Blog.routes.get('new_post')))

    def show_post(self, post_id=None):
        post = BlogPost.by_id(int(post_id))
        if post:
            if post.owner == self.user.key:
                self.render_internal('blog/read-post-by-owner.html',
                                      post=post,
                                      home=self.uri_for(Blog.routes.get('index')),
                                      edit_post=self.uri_for(Blog.routes.get('edit_post'), post_id=post_id))
            else:
                self.render_internal('blog/read-post-by-other.html',
                                      post=post,
                                      home=self.uri_for(Blog.routes.get('index')))
        else:
            self.error(404)
            return

    def modify_post(self, post_id=None):
        print 'modify_post'
        pass
