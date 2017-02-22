import webapp2

class Blog(webapp2.RequestHandler):

    @staticmethod
    def get_config():
        return {
            'blog_index_route': 'home'
        }
