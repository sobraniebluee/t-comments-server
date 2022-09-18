from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.db import Base, session, db
from src.models._mixins import Timestamp
from src.utils import random_id


class PostLikes(Base, Timestamp):
    __tablename__ = 'post_likes'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SMALLINT, nullable=False)
    id_post = db.Column(db.BIGINT, db.ForeignKey('posts.id', ondelete='CASCADE'))
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE"))

    def __init__(self, id_post, id_user, type):
        self.id_user = id_user
        self.id_post = id_post
        self.type = type

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class Post(Base, Timestamp):
    __tablename__ = 'posts'

    id = db.Column(db.BIGINT, primary_key=True)
    id_author = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.VARCHAR(300), nullable=False)
    description = db.Column(db.JSON, nullable=True)
    author = relationship('User', backref='posts', uselist=False)

    @property
    def rating(self):
        try:
            return (session.query(func.sum(PostLikes.type).label('type')).filter(PostLikes.id_post == self.id).first())['type']
        except Exception:
            raise

    def __init__(self, id_author, title, description):
        self.id = random_id()
        self.title = title
        self.description = description
        self.id_author = id_author
        self.is_voted = 0

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    # Save changes

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    # Count ratings for one Post

    @classmethod
    def one_of(cls, id_post):
        post = cls.query.filter(cls.id == id_post).first()
        if not post:
            return None
        rating, = session.query(func.sum(
            PostLikes.type
        )).filter(PostLikes.id_post == id_post).first()

        post.rating = rating if rating else 0
        return post

    def check_is_voted(self, id_user):
        if not id_user:
            self.is_voted = 0
            return
        post_like = PostLikes.query.filter(PostLikes.id_post == self.id, PostLikes.id_user == id_user).first()
        if not post_like:
            self.is_voted = 0
            return
        else:
            self.is_voted = post_like.type
            return

    def __repr__(self):
        return f'<Post id="{self.id}" title="{self.title}">'
