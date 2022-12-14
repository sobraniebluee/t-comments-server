from marshmallow import Schema, fields, post_dump, post_load
from src.config import Config


class ArgsPagination(Schema):
    page = fields.String(load_only=True)
    limit = fields.String(load_only=True)

    @post_load
    def data(self, data, **kwargs):
        if 'page' in data:
            try:
                data['page'] = int(data['page'])
            except Exception:
                data['page'] = 0
            if data['page'] < 1:
                data['page'] = 1
            if data['page']:
                data['page'] = data['page'] - 1
        else:
            data['page'] = 0
        if 'limit' in data:
            try:
                data['limit'] = int(data['limit'])
            except Exception:
                data['limit'] = Config.DEFAULT_LIMIT_PER_PAGE
        return data


class PaginationSchema(Schema):
    current_page = fields.Integer(dump_only=True)
    total_pages = fields.Integer(dump_only=True)
    total_entries = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)

    @post_dump
    def data(self, data, **kwargs):
        if 'current_page' in data:
            data['current_page'] = data['current_page'] + 1
        return data
