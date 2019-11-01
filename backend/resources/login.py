import falcon
import hashlib

from models.worker import Worker
from db.session import Session as session
from libs.auth import make_session, remove_session, auth_required
from libs.decorators import with_body_params
from schemas.worker import *
from config import config


class LoginController(object):

    @with_body_params(LoginSchema)
    def on_post(self, req, resp):

        ean13 = req.parsed['ean13']
        password = req.parsed['password']

        worker = session.query(Worker)\
            .filter(Worker.ean13 == ean13)\
            .filter(Worker.password == password)

        if not worker.scalar():
            raise falcon.HTTPForbidden()

        try:
            # import pdb; pdb.set_trace()
            resp.set_cookie(
                'user_session',
                make_session(
                    credential=str(ean13),
                    user_data=req.host + req.user_agent,
                    user_id=worker[0].id
                ),
                path='/'
            )
        except Exception:
            raise falcon.HTTPUnauthorized()


class LogoutController(object):

    @falcon.before(auth_required)
    def on_get(self, req, resp):

        remove_session(req.cookies['user_session'])


class CurrentUserController(object):

    @falcon.before(auth_required)
    def on_get(self, req, resp):

        resp.body = WorkerPublicSchema().dumps(self.user)
