import os
import jinja2

class TemplateRenderer:

    def __init__(self, template_dir='../templates'):
        template_path = os.path.join(os.path.dirname(__file__), template_dir)
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                                            autoescape=True)

    def render(self, template, **params):
        t = self.jinja_env.get_template(template)
        return t.render(params)
