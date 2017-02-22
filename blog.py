import webapp2

class Blog(webapp2.RequestHandler):

    @staticmethod
    def get_index_route():
        """ Index or starting route for this module """
        return 'home'
