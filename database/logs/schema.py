
from marshmallow_sqlalchemy import SQLAlchemySchema

from database.logs.model import Logs
from database.database import db
from marshmallow import fields

class LogsSchema(SQLAlchemySchema):
    class Meta:
        model = Logs
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    action = fields.String(required=True)
    ip = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)



