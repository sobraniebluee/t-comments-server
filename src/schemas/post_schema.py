from marshmallow import Schema, fields, validate, post_dump

from src.schemas.user_schema import UserSchema
from src.schemas.pagination_schema import PaginationSchema


class PostLikesSchema(Schema):
    id = fields.String(dump_only=True)
    type = fields.Integer(dump_only=True)
    id_post = fields.Integer(dump_only=True)
    id_user = fields.String(dump_only=True)


class ResponsePostSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)
    description = fields.Field(dump_only=True)
    author = fields.Nested(UserSchema(many=False, only=("id", "username",)))
    rating = fields.Integer(dump_only=True)
    is_voted = fields.Integer(dump_only=True)
    message = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

    @post_dump
    def check_rating(self, data, **kwargs):
        # if 'rating' not in data and 'message' not in data:
        #     data['rating'] = 0
        return data


class RequestCreatePostSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=3, max=299))
    description = fields.Field(required=False, validate=validate.Length(max=9999))


class ResponseAllPostsSchema(Schema):
    items = fields.Nested(ResponsePostSchema(many=True))
    pagination = fields.Nested(PaginationSchema(many=False))
    message = fields.String(dump_only=True)
