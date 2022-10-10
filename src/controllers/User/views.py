from flask import Blueprint
from src.services.user_service import UserService
from src.schemas.user_schema import AuthSchema, RegisterSchema, ResponseAuthSchema, JWT, UserSchema
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.middlewares.WithJwtCookies import with_jwt_cookies
user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
@with_jwt_cookies()
@use_kwargs(AuthSchema)
@marshal_with(ResponseAuthSchema)
def user_login(**kwargs):
    return UserService.login(**kwargs)


@user.route('/register', methods=['POST'])
@with_jwt_cookies()
@use_kwargs(RegisterSchema)
@marshal_with(ResponseAuthSchema)
def user_register(**kwargs):
    return UserService.register(**kwargs)


@user.route('/refresh', methods=['GET'])
@with_jwt_cookies()
@marshal_with(JWT)
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    return UserService.refresh(identity)


@user.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    identity = get_jwt_identity()
    return UserService.logout(identity)


@user.route('/protected', methods=['GET'])
@jwt_required()
def prot():
    return get_jwt_identity(), 200


@user.route('/me', methods=['GET'])
@jwt_required()
@marshal_with(UserSchema)
def me():
    identity = get_jwt_identity()
    return UserService.me(identity)
