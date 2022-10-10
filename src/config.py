import datetime


class FlaskConfig:
    SECRET = '83776601-7d7f-43f5-8ec9-bc3335fc9d2b'
    JWT_SECRET_KEY = '83776601-7d7f-43f5-8ec9-bc3335fc9d2b'
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    JWT_ERROR_MESSAGE_KEY = 'message'
    URL_PREFIX = "/api/v1"
    CACHE_TYPE = "memcached"
    # CACHE_TYPE = "simple"


class Config:
    DB_CONN = 'mysql+pymysql://sobranie:root@localhost/comments_api'
    LIKE = 1
    DISLIKE = -1
    CHANGE_TOGGLE = 'change'
    CREATE_TOGGLE = 'create'
    REMOVE_TOGGLE = 'remove'
    DEFAULT_LIMIT_PER_PAGE = 24
