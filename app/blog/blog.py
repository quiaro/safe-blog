import webapp2

from app.models.blogpost import BlogPost
from app.authenticated_handler import AuthenticatedHandler
import app.blog.constants as BlogConst


class Blog(AuthenticatedHandler):

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/blog',
                          handler=Blog,
                          handler_method='home',
                          methods=['GET'],
                          name=BlogConst.ROUTE_INDEX),

            webapp2.Route(r'/blog/new-post',
                          handler='app.blog.new_post.NewPost',
                          name=BlogConst.ROUTE_NEW_POST),

            webapp2.Route(r'/blog/<post_id>',
                          handler='app.blog.view_post.ViewPost',
                          name=BlogConst.ROUTE_VIEW_POST),

            webapp2.Route(r'/blog/<post_id>/edit',
                          handler='app.blog.edit_post.EditPost',
                          name=BlogConst.ROUTE_EDIT_POST),

            webapp2.Route(r'/blog/<post_id>/delete',
                          handler='app.blog.delete_post.DeletePost',
                          name=BlogConst.ROUTE_DELETE_POST),

            webapp2.Route(r'/comment/<comment_str>/update',
                          handler='app.blog.comment.Comment:update',
                          methods=['POST'],
                          name=BlogConst.ROUTE_UPDATE_COMMENT),

            webapp2.Route(r'/comment/<comment_str>/delete',
                          handler='app.blog.comment.Comment:delete',
                          methods=['POST'],
                          name=BlogConst.ROUTE_DELETE_COMMENT),
        ]

    def home(self):
        my_posts = BlogPost.created_by(self.user)
        other_posts = BlogPost.not_created_by(self.user)
        edit_post_fn = lambda p: self.uri_for(BlogConst.ROUTE_EDIT_POST, post_id=p.key.id())
        view_post_fn = lambda p: self.uri_for(BlogConst.ROUTE_VIEW_POST, post_id=p.key.id())
        self.render_internal('blog/home.html',
                              my_posts=my_posts,
                              other_posts=other_posts,
                              edit_post_fn=edit_post_fn,
                              view_post_fn=view_post_fn,
                              new_post=self.uri_for(BlogConst.ROUTE_NEW_POST))
