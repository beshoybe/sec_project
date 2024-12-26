

import datetime
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restful import Resource

from database.user.model import User
from resources.decorators.jwt_decorator import jwt_needed
from services.crypto_utils import decrypt_data, encrypt_data


class UserVerifyOtpApi(Resource):
    @jwt_needed
    def post(self):
        encrypted_data = request.get_json.get("encrypted_data")
        hmac_digest = request.get_json.get("hmac")
        data = decrypt_data(encrypted_data, hmac_digest)
        otp = data.get('otp')
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'encrypted_data':encrypt_data(data={'message': 'User not found'}) }, 404
        if user.otp == otp:
            user.update({'otp': None,'verified':True})
            jwt = create_access_token(identity=user.id, additional_claims={'role': user.role},expires_delta= datetime.timedelta(minutes=60))
            return {'encrypted_data':encrypt_data(data={'message': 'User verified successfully','access_token':jwt})}, 200
        return {'encrypted_data':encrypt_data(data={'message': 'Invalid OTP'})}, 400
    

        
        
        