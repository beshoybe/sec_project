
from flask import Flask
from flask_jwt_extended import JWTManager 
import os
from flask_mail import Mail
from flask_cors import CORS
import logging

app = Flask(__name__)

# CORS Configuration
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = None
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



# Mail Configuration
mail:Mail = Mail()
logging.getLogger('flask_cors').level = logging.DEBUG


def init_app():
    os.environ['ENV_FILE_LOCATION']='.env'
    app.config.from_envvar('ENV_FILE_LOCATION')
    mail.init_app(app)
    # JWT Configuration
    jwt = JWTManager(app) 

    return app
