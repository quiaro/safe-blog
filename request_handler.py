import os
import webapp2
import jinja2

from auth_helper import AuthHelper


class RequestHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                            autoescape=True)
        self.auth_helper = AuthHelper()
        super(RequestHandler, self).__init__(request, response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = self.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_internal(self, template, **kw):
        """
            For authorized users, templates are expected to extend from the
            layout/internal.html template. This method is used to provide any
            template that extends from layout/internal.html with any data that
            it requires (e.g. logout url and user entity)
        """
        kw['logout'] = self.uri_for(self.app.config.get('default_route_logout'))
        kw['user'] = self.user
        self.render(template, **kw)
