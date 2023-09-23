from aiohttp import web
from service.entities.api import aiohttp_routes


class WebServer:
    def __init__(self, app, middlewares, port=None):
        self._app = app
        if port is None:
            self._port = 8080
        else:
            self._port = int(port)

        self._web = web.Application(middlewares=middlewares)

        self._set_routes()

        web.run_app(self._web, port=self._port)

    @property
    def port(self):
        return self._port

    def _set_routes(self):
        self._web.add_routes(aiohttp_routes)
