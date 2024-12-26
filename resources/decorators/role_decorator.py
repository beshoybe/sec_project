
from functools import wraps

from jwt.exceptions import DecodeError,ExpiredSignatureError
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from flask_jwt_extended.exceptions import NoAuthorizationError


def role_needed(roles:list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(locations='headers')
            except (ValueError, DecodeError, TypeError, ExpiredSignatureError):
                return  {'message':'Wrong or Expired Token'},401
            except NoAuthorizationError:
                return {
        'message':'Token is missing from headers'},401
            claims = get_jwt()
            if claims.get('role') not in roles:
                return {'message':'You are not authorized to access this resource'},403
            return func(*args, **kwargs)
        return wrapper
    return decorator