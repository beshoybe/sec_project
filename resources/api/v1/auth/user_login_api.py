

import datetime
from flask import jsonify, render_template, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from database.logs.model import Logs
from database.logs.schema import LogsSchema
from database.user.logs_relationship import LogsUserRelationship
from database.user.model import User
from services.crypto_utils import decrypt_data, encrypt_data
from services.mail_service import send_email
from services.otp_service import generate_otp


class UserLoginApi(Resource):
    def post(self):
        encrypted_data = request.get_json.get("encrypted_data")
        hmac_digest = request.get_json.get("hmac")
        data = decrypt_data(encrypted_data, hmac_digest)
        log_schema = LogsSchema()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id,expires_delta= datetime.timedelta(minutes=3),additional_claims={'role': user.role})
            mail = user.email
            otp = generate_otp()
            user.update({'otp': otp})
            send_email('[SEC] Verify your account',
                sender=('SEC','logharitm.egy@gmail.com'),
                recipients=[mail],
                text_body=render_template('otp.txt',otp=otp),
                html_body=render_template('otp.html',otp=otp))
            log = log_schema.load({
                        'action': 'Login OTP Sent',
                        'ip': request.remote_addr,
                    })
            log = Logs(log)
            log.save()
            log_relationship = LogsUserRelationship({
                'log_id': log.id,
                'user_id': user.id,
                'created_by': None
            })
            log_relationship.save()
            return jsonify({'encrypted_data':encrypt_data(data={'message': 'OTP sent successfully','access_token':access_token})}), 200
        log = log_schema.load({
                    'action': 'Login Failed',
                    'ip': request.remote_addr,
             
        })
        log = Logs(log)
        log.save()
        log_relationship = LogsUserRelationship({
            'log_id': log.id,
            'user_id': user.id if user else None,
            'created_by': None
        })
        return {'encrypted_data':encrypt_data(data={'error': 'Invalid credentials'})}, 401