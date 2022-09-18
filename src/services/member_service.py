from src.models.user_model import User
from src.middlewares.Errors import Errors
from src.models.post_model import Post


class MemberService:
    @classmethod
    def get_user(cls, username):
        user = User.query.filter(User.username == username).first()
        if not user:
            return Errors.error_not_found()
        return user, 200

    @classmethod
    def get_user_posts(cls, username, identity=None):
        response, status_code = cls.get_user(username)
        if status_code == 200:
            user_id = response.id
            posts = Post.query.filter(Post.id_author == user_id).all()
            for post in posts:
                post.check_is_voted(identity)
            return posts, 200
        else:
            return [], 200

