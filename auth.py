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
    routes = dict(
        index='login',
        process_login='process_login',
        process_signup='process_signup',
    )
    login_key = 'login'
    signup_key = 'signup'

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/process-login',
                          handler=Auth,
                          handler_method='process_login',
                          methods=['POST'],
                          name=Auth.routes.get('process_login')),

            webapp2.Route(r'/process-signup',
                          handler=Auth,
                          handler_method='process_signup',
                          methods=['POST'],
                          name=Auth.routes.get('process_signup')),

            webapp2.Route('/login',
                          handler=Auth,
                          handler_method='login',
                          methods=['GET'],
                          name=Auth.routes.get('index')),

            webapp2.Route(r'/',
                          handler=Auth,
                          handler_method='index',
                          methods=['GET'],
                          name='index'),
        ]

    def _validate_signup(self, username, password, verify, email):
        """
            Checks if the form fields for the signup form are valid.
            Returns a dict with all the form fields plus a dict with errors.
            If any of the form fields were invalid, the error dict will store
            the form field name as the key and the error message as the value.
        """
        # Preseve form values for the user
        result = {
            'username': username,
            'email': email,
        }
        errors = {}

        # Check if the user already exists
        user = User.by_username(username)

        if user:
            errors['username'] = "Username already exists."

        if not valid_username(username):
            errors['username'] = "Invalid username."

        if not valid_password(password):
            errors['password'] = "Invalid password."

        elif password != verify:
            errors['verify'] = "Your passwords didn't match."

        if not valid_email(email):
            errors['email'] = "Invalid email."

        result['errors'] = errors
        return result

    def _grant_access(self, user):
        self.auth_helper.set_auth_cookie(self.response, user.key.string_id())
        return self.redirect_to(self.app.config.get('default_route_internal'))

    def process_login(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.authenticate(username, password)
        if not user:
            form_data = {
                'username': username,
                'errors': {
                    'general': 'User/password combination is invalid.'
                }
            }
            self.app.registry[Auth.login_key] = form_data
            return self.redirect_to(Auth.routes.get('index'))
        else:
            self._grant_access(user)

    def process_signup(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        form_data = self._validate_signup(username, password, verify, email)

        if len(form_data.get('errors').keys()) == 0:
            user = User.register(username, password, email)
            try:
                user.put()
            except TransactionFailedError:
                form_data['errors']['general'] = 'Unable to save entity. Please try again or contact your system administrator.'
            else:
                self._grant_access(user)

        # If there was an error, redirect back to this module's index route.
        # Store errors in the app registry so that they persist after the
        # redirect to display them.
        self.app.registry[Auth.signup_key] = form_data
        return self.redirect_to(Auth.routes.get('index'))

    def login(self):
        login_data = self.app.registry.get(Auth.login_key)
        signup_data = self.app.registry.get(Auth.signup_key)

        data = {
            Auth.login_key: login_data if login_data else { 'errors': {} },
            Auth.signup_key: signup_data if signup_data else { 'errors': {} }
        }

        self.render('login.html',
                    process_login=self.uri_for(Auth.routes.get('process_login')),
                    process_signup=self.uri_for(Auth.routes.get('process_signup')),
                    **data)

        # Clean up any errors stored in the registry
        self.app.registry[Auth.login_key] = None
        self.app.registry[Auth.signup_key] = None

    def index(self):
        user = self.auth_helper.get_authenticated_user(self.request)
        if user:
            # if already authorized, redirect to default_route_internal
            self.redirect_to(self.app.config.get('default_route_internal'))
        else:
            self.redirect(self.uri_for(Auth.routes.get('index')))
