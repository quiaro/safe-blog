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
        self.response.out.write('Processing login ...')

    def signup(self):
        """
            Process any incoming sign up requests
        """
        username = self.request.get('signup-username')
        password = self.request.get('signup-password')
        verify = self.request.get('signup-verify')
        email = self.request.get('signup-email')

        params = dict(username=username,
                      email=email,
                      errors={})

        # Check if the user already exists
        user = User.get_by_key_name(username)

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
            self.render('signup.html', **params)
        else:
            pwdHash = make_pwd_hash(username, password)

            # Create user (save pwdHash instead of password)
            user = User(key_name=username,
                        username=username,
                        password=pwdHash)
            try:
                user.put()
            except TransactionFailedError:
                errors[
                    'general'] = 'Unable to save entity. Please try again or contact your system administrator.'
                self.render('signup.html', **params)
                return

            self.login(username)


        self.response.out.write('Processing sign up ...')
