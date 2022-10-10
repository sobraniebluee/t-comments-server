import jwt

from src.config import FlaskConfig
from src.middlewares.Errors import Errors
from src.models.user_model import User, UserJwt


class UserService:
    @classmethod
    def login(cls, username, password):
        user = User.auth(username, password)
        if user:
            tokens = cls.get_tokens(user.id)
            data = {
                'data': user,
                'jwt': tokens
            }
            return data, 200
        else:
            return Errors.error_default('Sorry, your data wrong!', 400)

    @classmethod
    def register(cls, username, password, email):
        check_username = User.query.filter(User.username == username).first()
        if check_username:
            return Errors.error_default("Sorry, this username already used!", 400)
        new_user = User(username, password, email)
        new_user.save()

        return cls.login(new_user.username, password)

    @classmethod
    def get_tokens(cls, identity):
        user_tokens = UserJwt.query.filter(UserJwt.id_user == identity).first()
        if user_tokens:
            setattr(user_tokens, 'access_token', UserJwt.create_access_token(identity))
            setattr(user_tokens, 'refresh_token', UserJwt.create_refresh_token(identity))
            user_tokens.commit()
            return user_tokens
        else:
            user_tokens = UserJwt(id_user=identity)
            user_tokens.save()
            return user_tokens

    @classmethod
    def refresh(cls, identity):
        check_username = User.query.filter(User.id == identity).first()
        if not check_username:
            return Errors.error_default("", 401)
        return cls.get_tokens(identity)

    @classmethod
    def verification_token(cls, jwt_headers, jwt_payload):
        identity = jwt_payload.get('sub', None)
        is_user = User.query.filter(User.id == identity).first()
        if not is_user:
            return False
        user_tokens = UserJwt.query.filter(UserJwt.id_user == is_user.id).first()
        if not user_tokens:
            return False
        token_encode = jwt.encode(jwt_payload, FlaskConfig.JWT_SECRET_KEY, algorithm=jwt_headers['alg'])
        if user_tokens.access_token == token_encode or user_tokens.refresh_token == token_encode:
            return True
        else:
            return False

    @classmethod
    def logout(cls, identity):
        user_tokens = UserJwt.query.filter(UserJwt.id_user == identity).first()
        print(user_tokens)
        if not user_tokens:
            return Errors.error_default('Error logout', 400)
        user_tokens.delete()
        return '', 204

    @classmethod
    def me(cls, identity):
        user = User.query.filter(User.id == identity).first()
        if not user:
            return Errors.error_default('Error!', 401)
        return user, 200
