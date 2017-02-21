import webapp2

class Blog(webapp2.RequestHandler):

    @staticmethod
    def get_default_route():
        return 'home'
