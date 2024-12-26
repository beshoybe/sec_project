from marshmallow_sqlalchemy import SQLAlchemySchema
from database.database import db
from marshmallow import fields
from database.user.model import User
class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    name = fields.String(required=True)
    role = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    udpated_by = fields.String(dump_only=True)

