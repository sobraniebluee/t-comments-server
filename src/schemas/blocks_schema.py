from marshmallow import Schema, fields, validate


class BlocksOutputSchema(Schema):
    pass


class DataBlockOutputSchema(Schema):
    pass


class BlockOutputSchema(Schema):
    id = fields.String()
    type = fields.String(validate=validate.OneOf('paragraph', 'header'))
    data = fields.Nested({})