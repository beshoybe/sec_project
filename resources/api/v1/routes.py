

from flask_restful import Api

from resources.api.v1.auth.user_login_api import UserLoginApi
from resources.api.v1.auth.user_login_verify_otp_api import UserVerifyOtpApi
from resources.api.v1.auth.user_signup_api import UserSignupApi


def initialize_v1_routes(api:Api):
    api.add_resource(UserSignupApi, '/api/v1/auth/signup')
    api.add_resource(UserLoginApi, '/api/v1/auth/login')
    api.add_resource(UserVerifyOtpApi, '/api/v1/auth/verify_otp')
