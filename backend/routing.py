import falcon

from resources.index import *
from resources.activity_log import ActivityController
from resources.login import *


def make_route(app):

    app.add_route('/', IndexController())
    app.add_route('/activity', ActivityController())
    app.add_route('/login', LoginController())
    app.add_route('/logout', LogoutController())
    app.add_route('/users/current', CurrentUserController())
