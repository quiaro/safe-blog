from app.authenticated_handler import AuthenticatedHandler
from app.blog.blog import Blog
from app.models.blogpost import BlogPost
from app.models.comment import Comment
import app.blog.constants as BlogConst


class ViewPost(AuthenticatedHandler):

    def get_favorite_value(self, post, new_favorite_value):
        """
            Sets/unsets a post as favorited by a user per 'new_favorite_value'
            which can be a string equal to 'true' or 'false'. If
            'new_favorite_value' is not set, then the DB is queried to find the
            existing value.
        """
        user = self.user;

        if new_favorite_value:
            if new_favorite_value == 'true':
                user.add_favorite(post)
                is_favorite = True
            else:
                user.remove_favorite(post)
                is_favorite = False
            # Save the updated favorite list for the user
            user.put()
        else:
            is_favorite = user.likes(post)
        return is_favorite

    def render_post(self, post, new_comment={}):
        """
            Determines which template to show when reading a post. There are
            certain differences (e.g. ability to edit the post, liking a post)
            depending on whether the user is the post owner or not.
        """
        edit_post = is_favorite = None
        comments = Comment.by_post(post).order(Comment.created)

        if post.owner == self.user.key:
            template = 'blog/read-post-by-owner.html'
            edit_post = self.uri_for(BlogConst.ROUTE_EDIT_POST, post_id=post.key.id())
        else:
            template = 'blog/read-post-by-other.html'
            # If a user likes a blog post, this change will come in the form of
            # a query param "favorite".
            is_favorite = self.get_favorite_value(post, self.request.GET.get('favorite'))

        self.render_internal(template,
                            post=post,
                            comments=comments,
                            is_favorite=is_favorite,
                            new_comment=new_comment,
                            edit_post=edit_post,
                            home=self.uri_for(BlogConst.ROUTE_INDEX))

    def get(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        self.render_post(post)

    def post(self, post_id=None):
        post = BlogPost.by_id(post_id)

        if not post:
            self.error(404)
            return

        comment_body = self.request.get('new-comment')
        if comment_body:
            comment = Comment(parent=post.key,
                              user=self.user.key,
                              content=comment_body)
            comment.put()
            self.redirect_to(BlogConst.ROUTE_VIEW_POST, post_id=post_id)
        else:
            new_comment = {
                'error': "Please type in a comment before submitting."
            }
            self.render_post(post, new_comment)
