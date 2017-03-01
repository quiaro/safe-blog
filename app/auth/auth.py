import re
import webapp2

from app.request_handler import RequestHandler
from app.models.user import User
import app.auth.constants as AuthConst

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
    login_key = 'login'
    signup_key = 'signup'

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/process-login',
                          handler=Auth,
                          handler_method='process_login',
                          methods=['POST'],
                          name=AuthConst.ROUTE_PROCESS_LOGIN),

            webapp2.Route(r'/process-signup',
                          handler=Auth,
                          handler_method='process_signup',
                          methods=['POST'],
                          name=AuthConst.ROUTE_PROCESS_SIGNUP),

            webapp2.Route('/login',
                          handler=Auth,
                          handler_method='login',
                          methods=['GET'],
                          name=AuthConst.ROUTE_INDEX),

            webapp2.Route('/logout',
                          handler=Auth,
                          handler_method='logout',
                          methods=['GET'],
                          name=AuthConst.ROUTE_LOGOUT),
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
            return self.redirect_to(AuthConst.ROUTE_INDEX)
        else:
            self._grant_access(user)

    def process_signup(self):
        # Username field will be converted to lowercase and stripped off
        # whitespace
        username = self.request.get('username').lower().strip()
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
        else:
            # If there was an error, redirect back to this module's index route.
            # Store errors in the app registry so that they persist after the
            # redirect to display them.
            self.app.registry[Auth.signup_key] = form_data
            return self.redirect_to(AuthConst.ROUTE_INDEX)

    def login(self):
        login_data = self.app.registry.get(Auth.login_key)
        signup_data = self.app.registry.get(Auth.signup_key)

        data = {
            Auth.login_key: login_data if login_data else { 'errors': {} },
            Auth.signup_key: signup_data if signup_data else { 'errors': {} }
        }

        self.render('auth/login.html', **data)

        # Clean up any errors stored in the registry
        self.app.registry[Auth.login_key] = None
        self.app.registry[Auth.signup_key] = None

    def logout(self):
        self.auth_helper.destroy_auth_cookie(self.response)
        return self.redirect_to(self.app.config.get('default_route_external'))
