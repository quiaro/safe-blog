import webapp2
from google.appengine.api import namespace_manager

from auth import Auth
from blog import Blog

# Maintain a specific datastore instance defined by a namespace
# For more information:
# https://cloud.google.com/appengine/docs/standard/python/multitenancy/
NAMESPACE = '__alpha__'
namespace_manager.set_namespace(NAMESPACE)

config = dict(
            default_route_external = Auth.routes.get('index'),
            default_route_internal = Blog.routes.get('index')
            )

# Build list of all routes in the app. Auth routes should go last because
# they include the default (catch-all) route
routes = Blog.get_routes()
routes += Auth.get_routes()

app = webapp2.WSGIApplication(routes = routes, debug=True, config=config)
