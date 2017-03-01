import webapp2
from google.appengine.api import namespace_manager

from app.auth.auth import Auth
from app.blog.blog import Blog
import app.auth.constants as AuthConst
import app.blog.constants as BlogConst

# Maintain a specific datastore instance defined by a namespace
# For more information:
# https://cloud.google.com/appengine/docs/standard/python/multitenancy/
NAMESPACE = '__alpha__'
namespace_manager.set_namespace(NAMESPACE)

config = dict(
            default_route_external = AuthConst.ROUTE_INDEX,
            default_route_internal = BlogConst.ROUTE_INDEX,
            default_route_logout   = AuthConst.ROUTE_LOGOUT
            )

# Build list of all routes in the app.
routes = Blog.get_routes()
routes += Auth.get_routes()
routes += [ webapp2.Route(r'/', handler='app.index.Index', name='index') ]

app = webapp2.WSGIApplication(routes = routes, debug=True, config=config)
