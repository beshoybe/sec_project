from flask_restful import Api
from .routes import  initialize_v1_routes
def init_api(app):
    api = Api(app=app, )
    initialize_v1_routes(api)
