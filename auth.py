import re
import webapp2

from request_handler import RequestHandler
from models.user import User


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)


class Auth(RequestHandler):
    """
        Manages authentication of a web app by processing sign in and
        sign up requests.
    """

    @staticmethod
    def get_index_route():
        """ Index or starting route for this module """
        return 'login'

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/process-login',
                            handler=Auth,
                            handler_method='process_login',
                            methods=['POST'],
                            name='submit_login_url'),

            webapp2.Route(r'/process-signup',
                            handler=Auth,
                            handler_method='process_signup',
                            methods=['POST'],
                            name='submit_signup_url'),

            webapp2.Route('/login',
                            handler=Auth,
                            handler_method='login',
                            methods=['GET'],
                            name=Auth.get_index_route()),

            webapp2.Route(r'/',
                            handler=Auth,
                            handler_method='index',
                            methods=['GET'],
                            name='index'),
        ]

    def process_login(self):
        self.response.out.write('Processing login ...')

    def process_signup(self):
        username = self.request.get('signup-username')
        password = self.request.get('signup-password')
        verify = self.request.get('signup-verify')
        email = self.request.get('signup-email')

        # Get routes from app configuration
        login_route = self.app.config.get('login_route')
        default_route = self.app.config.get('default_route')

        params = dict(username=username,
                      email=email,
                      errors={})

        # Check if the user already exists
        user = User.by_name(username)

        if user:
            params['errors']['username'] = "Username already exists."

        if not valid_username(username):
            params['errors']['username'] = "Invalid username."

        if not valid_password(password):
            params['errors']['password'] = "Invalid password."

        elif password != verify:
            params['errors']['verify'] = "Your passwords didn't match."

        if not valid_email(email):
            params['errors']['email'] = "Invalid email."

        if len(params['errors'].keys()) != 0:
            # If there was an error, redirect back to the login route
            return self.redirect_to(login_route, **params)
        else:
            # pwdHash = make_pwd_hash(username, password)

            # Create user (save pwdHash instead of password)

            # TODO: Implement
            # user = User.register(username, pwdHash, email)
            #
            # try:
            #     user.put()
            # except TransactionFailedError:
            #     errors[
            #         'general'] = 'Unable to save entity. Please try again or contact your system administrator.'
            #     self.render('signup.html', **params)
            #     return

            return self.redirect_to(default_route)

    def login(self):
        self.render('login.html',
                    submit_login_url=self.uri_for('submit_login_url'),
                    submit_signup_url=self.uri_for('submit_signup_url'),
                    errors={})

    def index(self):
        # TODO if authorized, redirect to home
        # TODO if not authorized, redirect to login
        self.redirect(self.uri_for(Auth.get_index_route()))
