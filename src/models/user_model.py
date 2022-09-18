import hashlib
import uuid

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy_utils import UUIDType

from src.db import db, Base, session
from src.models._mixins import Timestamp


class User(Base, Timestamp):
    __tablename__ = 'users'

    id = db.Column(UUIDType(binary=False), primary_key=True)
    email = db.Column(db.VARCHAR(64), nullable=False)
    username = db.Column(db.VARCHAR(32), nullable=False)
    password = db.Column(db.VARCHAR(250), nullable=False)

    def __init__(self, username, password, email):
        self.id = uuid.uuid4()
        self.email = email
        self.username = username
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def auth(cls, username, password):
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = cls.query.filter(cls.username == username, cls.password == password).first()
        if not user:
            return False
        return user

    # def create(self, username, password) -> tuple[bool, str]:
    #     check_username = self.query.filter(self.username == username).first()
    #     print(check_username)
    #     if check_username:
    #         return False, 'Sorry, this username already used!'
    #     else:
    #         self.save()
    #         return True, ''

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            return

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            return


class UserJwt(Base, Timestamp):
    __tablename__ = 'users_jwt'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE"))
    access_token = db.Column(db.VARCHAR(500))
    refresh_token = db.Column(db.VARCHAR(500))

    def __init__(self, id_user):
        self.id_user = id_user
        self.refresh_token = self.create_refresh_token(id_user)
        self.access_token = self.create_access_token(id_user)

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            return

    @classmethod
    def create_access_token(cls, identity):
        return create_access_token(identity=identity)

    @classmethod
    def create_refresh_token(cls, identity):
        return create_refresh_token(identity=identity)

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
