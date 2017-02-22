import re
import webapp2
from webapp2_extras import sessions

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

    @staticmethod
    def get_config():
        return {
            'auth_index_route': 'login',
            'webapp2_extras.sessions': {
                'secret_key': SECRET_KEY,
                'cookie_args': {
                    'httponly': True
                }
            }
        }

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
                          name=Auth.get_config()['auth_index_route']),

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
        login_route = self.app.config.get('auth_index_route')
        app_route = self.app.config.get('blog_index_route')

        session_store = sessions.get_store(request=self.request)
        form_data = session_store.get_session()

        form_data['username'] = username
        form_data['email'] = email
        form_data['signup_errors'] = {}

        # Check if the user already exists
        user = User.by_name(username)

        if user:
            form_data['signup_errors'][
                'username'] = "Username already exists."

        if not valid_username(username):
            form_data['signup_errors']['username'] = "Invalid username."

        if not valid_password(password):
            form_data['signup_errors']['password'] = "Invalid password."

        elif password != verify:
            form_data['signup_errors'][
                'verify'] = "Your passwords didn't match."

        if not valid_email(email):
            form_data['signup_errors']['email'] = "Invalid email."

        if len(form_data['signup_errors'].keys()) != 0:
            # If there was an error, redirect back to the login route
            # Pass all the information via a session cookie
            session_store.save_sessions(self.response)

            return self.redirect_to(login_route)
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

            return self.redirect_to(app_route)

    def login(self):
        # Other methods will process the data from the sign in or sign up form.
        # If the data is invalid, error messages and previous form data
        # will be stored in a secure cookie so that they can be passed on to
        # this handler after a redirect
        session_store = sessions.get_store(request=self.request)
        cookie_data = session_store.get_session()

        login_data = {
            'login_errors': {},
            'signup_errors': {}
        }
        # Override default data with cookie data, if there's any.
        if cookie_data:
            login_data.update(cookie_data)

        self.render('login.html',
                    submit_login_url=self.uri_for('submit_login_url'),
                    submit_signup_url=self.uri_for('submit_signup_url'),
                    **login_data)

        # Delete cookie since it's no longer necessary
        self.response.delete_cookie('session')

    def index(self):
        # TODO if authorized, redirect to home
        # TODO if not authorized, redirect to login
        self.redirect(self.uri_for(Auth.get_config()['auth_index_route']))
