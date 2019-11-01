from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session

from db.engine import engine
from libs.sqlalchemy import CustomQuery


Session = scoped_session(
    sessionmaker(
        bind=engine,
        query_cls=CustomQuery
    )
)


class SQLAlchemySessionManager:

    def __init__(self, Session):
        self.db_session = Session

    def process_resource(self, req, resp, resource, params):
        if req.method == 'OPTIONS':
            return

        req.context['db_session'] = self.db_session()

    def process_response(self, req, resp, resource, req_succeeded):
        if req.method == 'OPTIONS':
            return

        if req.context.get('db_session'):
            if not req_succeeded:
                req.context['db_session'].rollback()
            req.context['db_session'].close()
