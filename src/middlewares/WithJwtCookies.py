import json


def with_jwt_cookies(key='jwt'):
    def wrapper(func):
        def params(*args, **kwargs):
            result = func(*args, **kwargs)
            response_jwt = json.loads(result.__dict__['response'][0].decode('utf-8'))
            if result.__dict__['_status_code'] in (200, 201, 202, 203, 204):
                if key in response_jwt:
                    response_jwt = response_jwt[key]
                result.set_cookie('access_token', response_jwt.get('access_token', None))
                result.set_cookie('refresh_token', response_jwt.get('refresh_token', None))
            return result
        params.__name__ = func.__name__
        return params
    return wrapper