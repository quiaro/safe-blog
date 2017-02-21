import os
import re
import webapp2
import jinja2
import hashlib

from auth import Auth
from blog import Blog

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

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
        self.render('login.html', login_url=Auth.login_url, signup_url=Auth.signup_url)


config = dict(
    default_route = Blog.get_default_route(),
    login_route   = 'login'
)


# Build list of all routes in the app. Ensure the index (catch-all) route is
# the last one in the list
routes = Auth.get_routes()
routes += [
    webapp2.Route(r'/login', handler=Login, name=config['login_route']),
    webapp2.Route(r'/', handler=Index, name='index'),
]

app = webapp2.WSGIApplication(routes = routes, debug=True, config=config)
