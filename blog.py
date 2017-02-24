import webapp2

from request_handler import RequestHandler

class Blog(RequestHandler):

    routes = dict(
        index='blog',
        new_post='new_post',
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
                          handler=Blog,
                          handler_method='new_post',
                          methods=['POST'],
                          name=Blog.routes.get('new_post')),

            webapp2.Route(r'/blog/<post_id>',
                          handler=Blog,
                          handler_method='read_post',
                          methods=['GET'],
                          name=Blog.routes.get('show_post')),

            webapp2.Route(r'/blog/<post_id>',
                          handler=Blog,
                          handler_method='modify_post',
                          methods=['POST'],
                          name=Blog.routes.get('modify_post')),

            webapp2.Route(r'/blog/<post_id>/edit',
                          handler=Blog,
                          handler_method='edit_post',
                          methods=['GET', 'POST'],
                          name=Blog.routes.get('edit_post')),
        ]

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

    def home(self):
        self.render_internal('blog/home.html', new_post=self.uri_for(Blog.routes.get('new_post')))
