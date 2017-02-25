import os
import jinja2


class TemplateRenderer:

    template_path = os.path.join(os.path.dirname(__file__), '../templates')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                                   autoescape=True)

    @classmethod
    def render(cls, template, **params):
        t = cls.jinja_env.get_template(template)
        return t.render(params)
