from database.database import db

class LogsUserRelationship(db.Model):
    __tablename__ = 'logs_user_relationship'
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('logs.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<LogsUserRelationship %r>' % self.id
    
    def __init__(self,data):
        for key in data:
            setattr(self,key,data[key])
    
    def save(self):
        db.session.add(self)
        db.session.commit()