import falcon
import hashlib

from db.session import Session
from config import config
from models.worker import Worker
from libs.redis import Redis


def get_user(user_session):
    user_id = Redis.get(user_session)

    if not user_id:
        raise falcon.HTTPUnauthorized()

    return Session.query(Worker).filter(Worker.id == int(user_id)).one_or_none()


def inspector_required(req, resp, resource, params):
    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user:
        raise falcon.HTTPUnauthorized()

    if not user.type.value == 2:
        raise falcon.HTTPForbidden()

    resource.user = user


def auth_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user:
        raise falcon.HTTPUnauthorized()

    resource.user = user


def make_session(credential, user_data, user_id):
    user_credential = credential + config['secure']['salt_session'] + user_data

    session = hashlib.sha256(user_credential.encode()).hexdigest()

    Redis.set(session, user_id)

    return session


def remove_session(session):
    Redis.delete(session)
