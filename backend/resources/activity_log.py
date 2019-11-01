import falcon
from sqlalchemy.sql import exists, func
from sqlalchemy.orm import aliased

from db.session import Session as session
from libs.auth import inspector_required
from models.activity_log import ActivityLog
from models.worker import Worker
from schemas.activity_log import ActivityLogSchema


class ActivityController:

    @falcon.before(inspector_required)
    def on_get(self, req, resp):

        inspector = aliased(ActivityLog)

        day = req.params['day']

        query = session.query(
            func.sum(inspector.payload).label('payload_sum'),
            func.extract('hour', inspector.server_time).label('hour'),
            ActivityLog.worker_id.label('collector_id'),
            Worker
        )\
            .join(Worker, Worker.id == ActivityLog.worker_id)\
            .join(inspector, inspector.box_code == ActivityLog.box_code)\
            .filter(inspector.type == 'REVIEW')\
            .filter(ActivityLog.type == 'COLLECT')\
            .filter(func.date(inspector.server_time) == day)\
            .group_by(ActivityLog.worker_id, func.extract('hour', inspector.server_time), Worker)

        log_data = []

        for res in query:
            log_data.append(
                {
                    "payload_in_hour": res[0],
                    "hour": int(res[1]),
                    "worker_id": res[2],
                    "worker_data": res[3]
                }
            )

        result = {
            "payload_data": log_data,
            "amount": log_data.__len__()
        }

        resp.body = ActivityLogSchema().dumps(result)
