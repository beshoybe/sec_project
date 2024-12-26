from database.database import db
class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Logs %r>' % self.action
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action
        }
    def __init__(self,data):
        for key in data:
            setattr(self,key,data[key])
    def save(self):
        db.session.add(self)
        db.session.commit()