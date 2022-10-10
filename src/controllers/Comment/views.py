from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from src.services.comment_service import CommentService
from src.schemas.comments_schema import CommentResponse, CommentRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.middlewares.Auth import auth_required

comment = Blueprint('comments', __name__)


@comment.route('/<id_post>', methods=['GET'])
@marshal_with(CommentResponse(many=True))
def get_comments_for_post(id_post):
    return CommentService.get_all(id_post=id_post)


@comment.route('/<id_post>', methods=['POST'])
@jwt_required()
@use_kwargs(CommentRequest)
@marshal_with(CommentResponse(many=True))
def create_comment_for_post(id_post, **kwargs):
    identity = get_jwt_identity()
    return CommentService.create_one(id_post=id_post, id_user=identity, **kwargs)


@comment.route('/<id_comment>', methods=['PUT'])
@jwt_required()
@use_kwargs(CommentRequest)
def update_comment_for_post(id_comment):
    return '', 204


@comment.route('/<id_comments>/', methods=['DELETE'])
@jwt_required()
def delete_comment_for_post(id_comment):
    return '', 204

