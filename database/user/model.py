
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    otp = db.Column(db.String(8), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return '<User %r>' % self.email
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role
        }
    def __init__(self,data):
        for key in data:
            setattr(self,key,data[key])
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self,data):
        for key in data:
            setattr(self,key,data[key])
        db.session.commit()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    def check_password(self,password):
        return check_password_hash(self.password,password)