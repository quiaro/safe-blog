import webapp2

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)


class Auth(webapp2.RequestHandler):
    """
        Manages authentication of a web app by processing sign in and
        sign up requests.
    """

    # Static vars
    login_url = '/process-login'
    signup_url = '/process-signup'

    @staticmethod
    def get_routes():
        return [
            webapp2.Route(Auth.login_url, handler=Auth, handler_method='login', methods=['POST']),
            webapp2.Route(Auth.signup_url, handler=Auth, handler_method='signup', methods=['POST'])
        ]

    def login(self):
        """
            Process any incoming login requests
        """
        # print('param1 %s' % param1)
        self.response.out.write('Processing login ...')

    def signup(self):
        """
            Process any incoming sign up requests
        """
        # print('param1 %s' % param1)
        self.response.out.write('Processing sign up ...')
