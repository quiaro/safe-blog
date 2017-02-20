import os
import re
import webapp2
import jinja2
import hashlib

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Index(Handler):

    def get(self):
        # TODO if authorized, redirect to home
        # TODO if not authorized, redirect to login
        self.redirect(self.uri_for('login'))


class Login(Handler):
    def get(self):
        self.render('login.html')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/login', handler=Login, name='login'),
    webapp2.Route(r'/', handler=Index, name='index'),
], debug=True)
