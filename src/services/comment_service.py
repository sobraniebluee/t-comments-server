from src.models.comment_model import Comment
from src.models.post_model import Post
from src.middlewares.Errors import Errors
from src.schemas.comments_schema import CommentResponse
from marshmallow import Schema


class CommentService:
    @classmethod
    def get_all(cls, id_post):
        comments = Comment.query.filter(Comment.id_post == id_post, Comment.is_reply == False).all()
        return comments, 200

    @classmethod
    def create_one(cls, id_post, id_user, text, id_root, is_reply):
        post = Post.query.filter(Post.id == id_post).first()
        if not post:
            return Errors.error_not_found(msg="Post not found!")
        if is_reply:
            root_post = Comment.query.filter(Comment.id_post == id_post, Comment.id == id_root).first()
            if not root_post:
                return Errors.error_default(msg="Sorry, this comment doesn't exist", status_code=400)

        comment = Comment(id_post=id_post,
                          id_root=id_root,
                          id_author=id_user,
                          text=text,
                          is_reply=is_reply)
        comment.save()
        return comment, 200

    @classmethod
    def delete_one(cls, id_comment):
        return '', 204

    @classmethod
    def update_one(cls, id_comment):
        return '', 204
