from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from schemas.worker import WorkerPublicSchema
from models.activity_log import ActivityType
from models.activity_log import ActivityStatus


class ActivityLogNestedSchema(Schema):

    payload_in_hour = fields.Integer()
    hour = fields.Integer()
    worker_id = fields.Integer()
    worker_data = fields.Nested(WorkerPublicSchema)


class ActivityLogSchema(Schema):

    payload_data = fields.Nested(ActivityLogNestedSchema, many=True)
    amount = fields.Integer()
