import webapp2

from app.models.blogpost import BlogPost
from app.authenticated_handler import AuthenticatedHandler


class Blog(AuthenticatedHandler):

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/blog',
                          handler=Blog,
                          handler_method='home',
                          methods=['GET'],
                          name='blog_index'),

            webapp2.Route(r'/blog/new-post',
                          handler='app.blog.new_post.NewPost',
                          name='blog_new_post'),

            webapp2.Route(r'/blog/<post_id>',
                          handler='app.blog.view_post.ViewPost',
                          name='blog_view_post'),

            webapp2.Route(r'/blog/<post_id>/edit',
                          handler='app.blog.edit_post.EditPost',
                          name='blog_edit_post'),

            webapp2.Route(r'/blog/<post_id>/delete',
                          handler='app.blog.delete_post.DeletePost',
                          name='blog_delete_post'),

            webapp2.Route(r'/blog/<post_id>/comment/<comment_id>/update',
                          handler='app.blog.comment.Comment:update',
                          methods=['POST'],
                          name='blog_update_comment'),

            webapp2.Route(r'/blog/<post_id>/comment/<comment_id>/delete',
                          handler='app.blog.comment.Comment:delete',
                          methods=['POST'],
                          name='blog_delete_comment'),
        ]

    def home(self):
        my_posts = BlogPost.created_by(self.user)
        other_posts = BlogPost.not_created_by(self.user)
        edit_post_fn = lambda p: self.uri_for('blog_edit_post', post_id=p.key.id())
        view_post_fn = lambda p: self.uri_for('blog_view_post', post_id=p.key.id())
        self.render_internal('blog/home.html',
                              my_posts=my_posts,
                              other_posts=other_posts,
                              edit_post_fn=edit_post_fn,
                              view_post_fn=view_post_fn,
                              new_post=self.uri_for('blog_new_post'))
