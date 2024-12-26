

from functools import wraps

from jwt.exceptions import DecodeError,ExpiredSignatureError
from flask_jwt_extended import verify_jwt_in_request

from flask_jwt_extended.exceptions import NoAuthorizationError

from services.crypto_utils import encrypt_data

def jwt_needed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request(locations='headers')
        except (ValueError, DecodeError, TypeError,ExpiredSignatureError ):
            return  {'encrypted_data':encrypt_data(data={'message':'Wrong or Expired Token'})},401
        except NoAuthorizationError:
            return {
    'encrypted_data':encrypt_data(data={'message':'Token is missing from headers'})},401
        return func(*args, **kwargs)
    return decorator