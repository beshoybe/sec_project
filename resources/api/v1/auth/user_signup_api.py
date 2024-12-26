

import datetime
from flask import render_template, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource

from database.user.model import User
from database.user.schema import UserSchema
from services.crypto_utils import decrypt_data
from services.mail_service import send_email
from services.otp_service import generate_otp


class UserSignupApi(Resource):
    jwt_required(optional=True),
    def post(self):
        encrypted_data = request.get_json.get("encrypted_data")
        hmac_digest = request.get_json.get("hmac")
        data = decrypt_data(encrypted_data, hmac_digest)
        user_schema = UserSchema()
        user = user_schema.load(data)
        if User.query.filter_by(email=user['email']).first():
            return {'message': 'User already exists'}, 400
        jwt = get_jwt_identity()
        if user['role'] == 'admin' and jwt is not None and jwt['role'] != 'admin':
            return {'message': 'You are not authorized to create an admin'}, 403
        user = User(user)
        user.hash_password()
        user.save()
        if user.role == 'user':
            otp = generate_otp()
            user.update({'otp': otp,'role':'user'})
            send_email('[SEC] Verify your account',
                    sender=('SEC','logharitm.egy@gmail.com'),
                    recipients=[user.email],
                    text_body=render_template('otp.txt',otp=otp),
                    html_body=render_template('otp.html',otp=otp))
            access_token = create_access_token(identity=user.id,expires_delta= datetime.timedelta(minutes=3),additional_claims={'role': user.role})
            return {'message': 'User created successfully','access_token':access_token}, 201
        return {'message': 'User created successfully'}, 201