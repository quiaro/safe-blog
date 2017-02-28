import webapp2

from app.models.blogpost import BlogPost
from app.authenticated_handler import AuthenticatedHandler


class Blog(AuthenticatedHandler):

    routes = dict(
        index='blog',
        new_post='new_post',
        edit_post='edit_post',
        delete_post='delete_post',
        view_post='view_post',
        post_comment='post_comment',
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
                          handler_method='view_post',
                          methods=['GET'],
                          name=Blog.routes.get('view_post')),

            webapp2.Route(r'/blog/<post_id>',
                          handler=Blog,
                          handler_method='post_comment',
                          methods=['POST'],
                          name=Blog.routes.get('post_comment')),
        ]

    def home(self):
        my_posts = BlogPost.created_by(self.user)
        other_posts = BlogPost.not_created_by(self.user)
        edit_post_fn = lambda p: self.uri_for(Blog.routes.get('edit_post'), post_id=p.key.id())
        view_post_fn = lambda p: self.uri_for(Blog.routes.get('view_post'), post_id=p.key.id())
        self.render_internal('blog/home.html',
                              my_posts=my_posts,
                              other_posts=other_posts,
                              edit_post_fn=edit_post_fn,
                              view_post_fn=view_post_fn,
                              new_post=self.uri_for(Blog.routes.get('new_post')))

    def get_favorite_value(self, user, post, new_favorite_value):
        """
            Sets/unsets a post as favorited by a user per 'new_favorite_value'
            which can be a string equal to 'true' or 'false'. If
            'new_favorite_value' is not set, then the DB is queried to find the
            existing value.
        """
        if new_favorite_value:
            if new_favorite_value == 'true':
                user.add_favorite(post)
                is_favorite = True
            else:
                user.remove_favorite(post)
                is_favorite = False
            # Save the updated favorite list for the user
            user.put()
        else:
            is_favorite = user.likes(post)
        return is_favorite

    def render_read_post(self, user, post, new_comment={}):
        """
            Determines which template to show when reading a post. There are
            certain differences (e.g. ability to edit the post, liking a post)
            depending on whether the user is the post owner or not.
        """
        edit_post = is_favorite = None;

        if post.owner == user.key:
            template = 'blog/read-post-by-owner.html'
            edit_post = self.uri_for(Blog.routes.get('edit_post'), post_id=post.key.id())
        else:
            template = 'blog/read-post-by-other.html'
            # If a user likes a blog post, this change will come in the form of
            # a query param "favorite".
            is_favorite = self.get_favorite_value(user, post, self.request.GET.get('favorite'))

        self.render_internal(template,
                            post=post,
                            comments=post.comments,
                            is_favorite=is_favorite,
                            new_comment=new_comment,
                            edit_post=edit_post,
                            home=self.uri_for(Blog.routes.get('index')))

    def view_post(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        self.render_read_post(self.user, post)

    def post_comment(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        new_comment = self.request.get('new-comment')
        if new_comment:
            post.add_comment(self.user, new_comment)
            post.put()
            self.redirect_to(Blog.routes.get('view_post'), post_id=post_id)
        else:
            new_comment = {
                'error': "Please type in a comment before submitting."
            }
            self.render_read_post(self.user, post, new_comment)
