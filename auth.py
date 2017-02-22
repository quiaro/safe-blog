import re
import webapp2

from secret import SECRET_KEY
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
    ROUTES = dict(
        index='login',
        process_login='process_login',
        process_signup='process_signup',
    )
    LOGIN_KEY = 'login'
    SIGNUP_KEY = 'signup'

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(r'/process-login',
                          handler=Auth,
                          handler_method='process_login',
                          methods=['POST'],
                          name=Auth.ROUTES.get('process_login')),

            webapp2.Route(r'/process-signup',
                          handler=Auth,
                          handler_method='process_signup',
                          methods=['POST'],
                          name=Auth.ROUTES.get('process_signup')),

            webapp2.Route('/login',
                          handler=Auth,
                          handler_method='login',
                          methods=['GET'],
                          name=Auth.ROUTES.get('index')),

            webapp2.Route(r'/',
                          handler=Auth,
                          handler_method='index',
                          methods=['GET'],
                          name='index'),
        ]

    def _validate_signup(self):
        """
            Checks if the form fields for the signup form are valid.
            Returns a dict with all the form fields plus a dict with errors.
            If any of the form fields were invalid, the error dict will store
            the form field name as the key and the error message as the value.
        """
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        # Preseve form values for the user
        result = {
            'username': username,
            'email': email,
        }
        errors = {}

        # Check if the user already exists
        user = User.by_name(username)

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

    def process_login(self):
        self.response.out.write('Processing login ...')

    def process_signup(self):
        form_data = self._validate_signup()

        if len(form_data.get('errors').keys()) != 0:
            # If there was an error, redirect back to the login route.
            # Store errors in the app registry so that they persist after
            # the redirect to display them.
            self.app.registry[Auth.SIGNUP_KEY] = form_data
            return self.redirect_to(self.app.config.get('default_route_external'))

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

            return self.redirect_to(self.app.config.get('default_route_internal'))

    def login(self):
        login_data = self.app.registry.get(Auth.LOGIN_KEY)
        signup_data = self.app.registry.get(Auth.SIGNUP_KEY)

        data = {
            Auth.LOGIN_KEY: login_data if login_data else { 'errors': {} },
            Auth.SIGNUP_KEY: signup_data if signup_data else { 'errors': {} }
        }

        self.render('login.html',
                    process_login=self.uri_for(Auth.ROUTES.get('process_login')),
                    process_signup=self.uri_for(Auth.ROUTES.get('process_signup')),
                    **data)

        # Clean up any errors stored in the registry
        self.app.registry[Auth.LOGIN_KEY] = None
        self.app.registry[Auth.SIGNUP_KEY] = None

    def index(self):
        # TODO if authorized, redirect to home
        # TODO if not authorized, redirect to login
        self.redirect(self.uri_for(Auth.ROUTES.get('index')))
