
from app import init_app
from database.database import init_database
from resources.api.v1.api import init_api

application = init_app()
init_database(application)
init_api(application)
if __name__ == '__main__':  
   application.run(debug=True,threaded=True)
   