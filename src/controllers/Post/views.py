from flask import Blueprint
from src.services.post_service import PostService
from flask_apispec import use_kwargs, marshal_with
from src.schemas.post_schema import ResponseAllPostsSchema, RequestCreatePostSchema, ResponsePostSchema
from src.schemas.pagination_schema import ArgsPagination
from src.middlewares.Pagination import pagination
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.config import Config
from src import cache
from src.middlewares.Auth import auth_required
posts = Blueprint('posts', __name__)

# GET ALL


@posts.route('', methods=['GET'])
# @cache.cached(timeout=10, key_prefix="get_all_posts")
@use_kwargs(ArgsPagination, location='query')
@marshal_with(ResponseAllPostsSchema)
@pagination(_limit=24)
@auth_required(optional=True)
def get_posts(identity):
    return PostService.get_all(identity)


# GET ONE

@posts.route('<id_post>', methods=['GET'])
@auth_required(optional=True)
@marshal_with(ResponsePostSchema)
def get_post(id_post, identity):
    return PostService.get_one(id_post, identity)


# CREATE

@posts.route('', methods=['POST'])
@jwt_required()
@use_kwargs(RequestCreatePostSchema)
@marshal_with(ResponsePostSchema)
def create_post(**kwargs):
    identity = get_jwt_identity()
    return PostService.create(id_author=identity, **kwargs)


# EDIT

@posts.route('<id_post>', methods=['PUT'])
@jwt_required()
@use_kwargs(RequestCreatePostSchema)
@marshal_with(ResponsePostSchema)
def edit_post(id_post, **kwargs):
    identity = get_jwt_identity()
    return PostService.edit(id_post=id_post, id_author=identity, **kwargs)


# TOGGLE SERVICE

@posts.route('<id_post>/dislike', methods=['POST'])
@jwt_required()
def dislike_post(id_post):
    identity = get_jwt_identity()
    return PostService.toggle(id_post=id_post, id_user=identity, type_mark=Config.DISLIKE)


@posts.route('<id_post>/like', methods=['POST'])
@jwt_required()
def like_post(id_post):
    identity = get_jwt_identity()
    return PostService.toggle(id_post=id_post, id_user=identity, type_mark=Config.LIKE)


# DELETE POST

@posts.route('<id_post>', methods=['DELETE'])
@jwt_required()
def delete_post(id_post):
    identity = get_jwt_identity()
    return PostService.delete(identity, id_post)

