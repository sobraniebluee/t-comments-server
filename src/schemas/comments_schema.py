from marshmallow import Schema, fields, validate, post_dump, pre_dump
from src.schemas.author_schema import AuthorSchema

# CREATE SCHEMA FOR BLOCKS!!!!!!!


class CommentResponse(Schema):
    id = fields.Integer(dump_only=True)
    id_post = fields.Integer(dump_only=True)
    id_author = fields.String(dump_only=True)
    id_root = fields.Integer(dump_only=True)
    author = fields.Nested(AuthorSchema)
    text = fields.Field(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    answers = fields.Nested('self', many=True)
    message = fields.String(dump_only=True)


class CommentRequest(Schema):
    text = fields.Field(required=True)
    id_root = fields.Field(required=True, allow_none=True)
    is_reply = fields.Boolean(required=True)
