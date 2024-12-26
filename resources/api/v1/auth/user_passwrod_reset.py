

import datetime
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restful import Resource

from database.user.model import User
from resources.decorators.jwt_decorator import jwt_needed
from services.crypto_utils import decrypt_data, encrypt_data


class UserPasswordResetApi(Resource):
    @jwt_needed
    def post(self):
        encrypted_data = request.get_json.get("encrypted_data")
        hmac_digest = request.get_json.get("hmac")
        data = decrypt_data(encrypted_data, hmac_digest) 
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'encrypted_data':encrypt_data(data={'message': 'User not found'}) }, 404
        password = data.get('password')
        user.update({'password':password})
        user.hash_password()
        user.save()
        access_token = create_access_token(identity=user.id,expires_delta= datetime.timedelta(minutes=60),additional_claims={'role': user.role})
        return {'encrypted_data':encrypt_data(data={'message': 'Password reset successfully','access_token':access_token})}, 200
        