from marshmallow import Schema, fields, validate


class JWT(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)


class AuthSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=32, error="Username must be in range 3 to 32 chars"))
    password = fields.String(required=True, validate=validate.Length(min=3, max=32, error="Password must be in range 3 to 32 chars"))


class RegisterSchema(AuthSchema):
    email = fields.String(required=True, error_messages={"required": "Hello"}, validate=validate.Email(error="Please, enter a valid email"))


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    message = fields.String(dump_only=True)


class ResponseAuthSchema(Schema):
    data = fields.Nested(UserSchema(many=False), dump_only=True)
    jwt = fields.Nested(JWT(many=False), dump_only=True)
    message = fields.String(dump_only=True)
