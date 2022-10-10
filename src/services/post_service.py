from src.config import Config
from src.middlewares.Errors import Errors
from src.models.post_model import Post, PostLikes
from sqlalchemy import asc, desc


class PostService:
    @classmethod
    def get_all(cls, id_user=None):
        posts = Post.query.order_by(desc(Post.created_at)).all()
        for item in posts:
            item.check_is_voted(id_user)
        return posts, 200

    # Return ID post
    @classmethod
    def create(cls, id_author, title, description=None):
        new_post = Post(id_author=id_author, title=title, description=description)
        new_post.save()
        return {"id": new_post.id}, 201

    @classmethod
    def get_one(cls, id_post, id_user=None):
        post = Post.query.filter(Post.id == id_post).first()
        if not post:
            return Errors.error_not_found()
        post.check_is_voted(id_user)
        return post, 200

    @classmethod
    def edit(cls, id_post, id_author, **kwargs):
        post = Post.query.filter(Post.id == id_post, Post.id_author == id_author).first()
        if not post:
            return Errors.server_error()
        for _, item in enumerate(kwargs):
            setattr(post, item, kwargs.get(item))
        post.commit()
        return post, 200

    @classmethod
    def delete(cls, identity, id_post):
        post = Post.query.filter(Post.id_author == identity, Post.id == id_post).first()
        if not post:
            return Errors.error_not_found()
        post.delete()
        return '', 204

    @classmethod
    def toggle(cls, id_post, id_user, type_mark):
        post = Post.query.filter(Post.id == id_post).first()
        if not post:
            return Errors.error_not_found()
        has_mark = PostLikes.query.filter(PostLikes.id_post == id_post, PostLikes.id_user == id_user).first()
        if not has_mark:
            new_mark = PostLikes(id_post=id_post, id_user=id_user, type=type_mark)
            new_mark.save()
            return {'status_toggle': Config.CREATE_TOGGLE}, 200
        opposite_mark = Config.LIKE if type_mark == Config.DISLIKE else Config.DISLIKE
        if has_mark.type == opposite_mark:
            setattr(has_mark, 'type', type_mark)
            has_mark.commit()
            return {'status_toggle': Config.CHANGE_TOGGLE}, 200
        if has_mark:
            has_mark.delete()
            return {'status_toggle': Config.REMOVE_TOGGLE}, 200


