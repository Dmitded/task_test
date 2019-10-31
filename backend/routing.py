import falcon

from resources.index import *


def make_route(app):

    app.add_route('/', IndexController())
