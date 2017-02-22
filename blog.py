import webapp2

class Blog(webapp2.RequestHandler):

    ROUTES = dict(
        index='home'
    )
