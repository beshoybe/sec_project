from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from database.user.model import User
from database.logs.model import Logs
from database.user.logs_relationship import LogsUserRelationship


def init_database(app):
    # app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://coderoen_saraya:elsaraya2024@127.0.0.1:3306/coderoen_elsaraya'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:password@127.0.0.1:3306/comp_sec'    
    db.init_app(app)
    with app.app_context():
        db.create_all()
