import webapp2

from auth import Auth
from blog import Blog

config = dict(
    app_index_route  = Blog.get_index_route(),
    auth_index_route = Auth.get_index_route()
)

# Build list of all routes in the app. Ensure the index (catch-all) route is
# the last one in the list
routes = Auth.get_routes()

app = webapp2.WSGIApplication(routes = routes, debug=True, config=config)
