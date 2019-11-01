from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.worker import WorkerType


class LoginSchema(Schema):

    ean13 = fields.Integer(required=True)
    password = fields.String(required=True)

    class Meta:
        type_ = "worker"


class WorkerPublicSchema(Schema):

    id = fields.Integer()
    ean13 = fields.String()
    name = fields.String()
    surname = fields.String()
    middle_name = fields.String()
    type = EnumField(WorkerType)
    deleted = fields.Boolean()

    class Meta:
        type_ = "worker"
