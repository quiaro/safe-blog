import os
import jinja2
import webapp2

import app.auth.constants as AuthConst
import app.blog.constants as BlogConst


class TemplateRenderer:

    template_path = os.path.join(os.path.dirname(__file__), '../templates')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                                   autoescape=True)
    jinja_env.globals = {
        'uri_for': webapp2.uri_for,
        'auth_routes': AuthConst,
        'blog_routes': BlogConst
    }

    @classmethod
    def render(cls, template, **params):
        t = cls.jinja_env.get_template(template)
        return t.render(params)
