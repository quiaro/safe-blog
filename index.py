from request_handler import RequestHandler

class Index(RequestHandler):
    """
        If the user has already authenticated, the GET handler in this class
        will redirect the user to the appropriate default internal route.
        If not, the user is redirected to the default external route so he
        can log in (or sign up) first.
    """

    def get(self):
        user = self.auth_helper.get_authenticated_user(self.request)
        if user:
            # if already authorized, redirect to default_route_internal
            self.redirect_to(self.app.config.get('default_route_internal'))
        else:
            self.redirect(self.app.config.get('default_route_external'))
