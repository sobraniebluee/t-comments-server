from flask import Blueprint
from src.services.member_service import MemberService
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_apispec import use_kwargs, marshal_with
from src.schemas.user_schema import UserSchema
from src.schemas.pagination_schema import ArgsPagination
from src.schemas.post_schema import ResponseAllPostsSchema
from src.middlewares.Pagination import pagination
member = Blueprint("members", __name__)


@member.route("/<username>", methods=["GET"])
@marshal_with(UserSchema)
def get_one_user(username):
    return MemberService.get_user(username=username)


@member.route("/<username>/posts", methods=["GET"])
@jwt_required(optional=True)
@use_kwargs(ArgsPagination, location="query")
@marshal_with(ResponseAllPostsSchema)
@pagination(_limit=24)
def get_user_post(username):
    # verify = verify_jwt_in_request(optional=True, verify_type=False)
    # print(verify)
    identity = get_jwt_identity()
    # identity = None
    return MemberService.get_user_posts(username=username, identity=identity)

