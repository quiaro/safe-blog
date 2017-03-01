import webapp2
from google.appengine.api import namespace_manager

from app.auth import Auth
from app.blog.blog import Blog

# Maintain a specific datastore instance defined by a namespace
# For more information:
# https://cloud.google.com/appengine/docs/standard/python/multitenancy/
NAMESPACE = '__alpha__'
namespace_manager.set_namespace(NAMESPACE)

config = dict(
            default_route_external = 'auth_index',
            default_route_internal = 'blog_index',
            default_route_logout   = 'auth_logout'
            )

# Build list of all routes in the app.
routes = Blog.get_routes()
routes += Auth.get_routes()
routes += [ webapp2.Route(r'/', handler='app.index.Index', name='index') ]

app = webapp2.WSGIApplication(routes = routes, debug=True, config=config)
