from app.request_handler import RequestHandler

class AuthenticatedHandler(RequestHandler):

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
