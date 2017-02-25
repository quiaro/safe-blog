import webapp2

from app.request_handler import RequestHandler
from app.models.blogpost import BlogPost


class AppSection(RequestHandler):

    def initialize(self, *a, **kw):
        """
            This method overrides webapp2.RequestHandler.initialize in order
            to check for the existence of the authentication cookie with every
            request. If the auth cookie exists, its value is deserialized and
            used to retrieve the user entity. If the user entity exists, it's
            attached to the request; otherwise, the user is redirected to the
            app's authentication index.
        """
        RequestHandler.initialize(self, *a, **kw)
        self.user = self.auth_helper.get_authenticated_user(self.request)
        if not self.user:
            return self.redirect_to(self.app.config.get('default_route_external'))


class Blog(AppSection):

    routes = dict(
        index='blog',
        new_post='new_post',
        edit_post='edit_post',
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
                          handler=NewPost,
                          name=Blog.routes.get('new_post')),

            webapp2.Route(r'/blog/<post_id>/edit',
                          handler=EditPost,
                          name=Blog.routes.get('edit_post')),

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
        self.render_internal('blog/home.html',
                              my_posts=my_posts,
                              other_posts=other_posts,
                              new_post=self.uri_for(Blog.routes.get('new_post')))

    def show_post(self, post_id=None):
        post = BlogPost.get_by_id(int(post_id), parent=self.user.key)
        if post:
            self.render_internal('blog/read-post.html',
                                  post=post,
                                  home=self.uri_for(Blog.routes.get('index')),
                                  edit_post=self.uri_for(Blog.routes.get('edit_post'), post_id=post_id))
        else:
            self.error(404)
            return

    def modify_post(self, post_id=None):
        print 'modify_post'
        pass


class NewPost(AppSection):

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
                         created_by=self.user.key)
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

class EditPost(AppSection):

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
