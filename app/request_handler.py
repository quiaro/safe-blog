import webapp2

from app.utils.auth_helper import AuthHelper
from app.utils.template_renderer import TemplateRenderer


class RequestHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.auth_helper = AuthHelper()
        super(RequestHandler, self).__init__(request, response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_template(self, template, **params):
        return TemplateRenderer.render(template, **params)

    def render(self, template, **kw):
        self.write(self.render_template(template, **kw))

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
