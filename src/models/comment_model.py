from src.db import db, Base, session
from src.models._mixins import Timestamp
from sqlalchemy_utils import UUIDType
from src.utils import random_id
from sqlalchemy.orm import relationship
from sqlalchemy import desc


class Comment(Base, Timestamp):
    __tablename__ = 'comments'

    id = db.Column(db.BIGINT, primary_key=True)
    id_post = db.Column(db.BIGINT, db.ForeignKey('posts.id', ondelete="CASCADE"))
    id_author = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'))
    id_root = db.Column(db.BIGINT, db.ForeignKey('comments.id', ondelete="CASCADE"), nullable=True)
    is_reply = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.JSON, nullable=False)
    author = relationship('User', backref='users.id', uselist=False)
    # answers = relationship('Comment', remote_side=[id_root], uselist=True)

    @property
    def answers(self):
        return session.query(Comment).filter(Comment.id_root == self.id, Comment.is_reply == True).order_by(desc(Comment.created_at)).all()

    def __init__(self, id_post, id_author, id_root, text, is_reply):
        self.id = random_id()
        self.id_post = id_post
        self.id_root = id_root
        self.is_reply = is_reply
        self.id_author = id_author
        self.text = text

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

    def __repr__(self):
        return f"<Comment id={self.id} id_post={self.id_post} id_root={self.id_root}>"
