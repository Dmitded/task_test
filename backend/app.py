import falcon

from db.session import Session, SQLAlchemySessionManager
from routing import make_route


app = falcon.API(
    middleware=[SQLAlchemySessionManager(Session)]
)

app.resp_options.secure_cookies_by_default = False

make_route(app)
