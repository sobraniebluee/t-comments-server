from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def auth_required(optional=False, refresh=False):
    """
    Check jwt and return identity to target function if jwt set,
    else return none and skip auth step
    Warning: Don't return Authenticated error, use instead jwt_required(optional=True)
    """
    def decorate(func):
        def args_decorate(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=optional, refresh=refresh)
                identity = get_jwt_identity()
            except Exception as e:
                identity = None

            result = func(identity=identity, *args, **kwargs)
            return result
        args_decorate.__name__ = func.__name__
        return args_decorate
    return decorate
