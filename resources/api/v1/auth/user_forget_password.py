

import datetime
from flask import render_template, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from database.user.model import User
from services.crypto_utils import decrypt_data, encrypt_data
from services.mail_service import send_email
from services.otp_service import generate_otp


class UserForgetPasswordApi(Resource):
    def post(self):
        encrypted_data = request.get_json.get("encrypted_data")
        hmac_digest = request.get_json.get("hmac")
        data = decrypt_data(encrypted_data, hmac_digest)
        email = data.get('email')
        #send otp
        user = User.query.filter_by(email=email).first()
        if user:
            otp = generate_otp()
            user.update({'otp': otp})
            
            send_email('[SEC] Verify your account',
                sender=('SEC','logharitm.egy@gmail.com'),
                recipients=[user.email],
                text_body=render_template('otp.txt',otp=otp),
                html_body=render_template('otp.html',otp=otp))
            access_token = create_access_token(identity=user.id,expires_delta= datetime.timedelta(minutes=3),additional_claims={'role': user.role})
            return {'encrypted_data':encrypt_data(data={'message': 'OTP sent successfully','access_token':access_token})}, 200
        else:
            return {'encrypted_data':encrypt_data(data={'message': 'User not found'}) }, 404