from webapp2_extras.securecookie import SecureCookieSerializer

from app.secret import SECRET_KEY
from app.models.user import User

class AuthHelper:

    def __init__(self):
        self.user_cookie = 'uc'
        self.secure_cookie_serializer = SecureCookieSerializer(SECRET_KEY)

    def get_authenticated_user(self, request):
        """
            Reads the auth cookie from the request and returns the user entity
            associated to the cookie value.
        """
        cookie_val = request.cookies.get(self.user_cookie)
        uid = self.secure_cookie_serializer.deserialize(self.user_cookie, cookie_val)
        return uid and User.by_username(uid)


    def set_auth_cookie(self, response, uid):
        """
            Takes a valid user id and sets a secure cookie (token) in the
            response used to validate if the user is signed in.
        """
        cookie_val = self.secure_cookie_serializer.serialize(self.user_cookie, uid)
        response.set_cookie(self.user_cookie, cookie_val, httponly=True)

    def destroy_auth_cookie(self, response):
        response.delete_cookie(self.user_cookie)
