from service.entities.api.web_server import WebServer
from aiohttp import web


class ApiManager:

    def __init__(self, app):
        self._app = app
        self._middlewares = []

        self._manage_middlewares()

        self.web_server = WebServer(app=self._app, middlewares=self._middlewares)

    def _manage_middlewares(self):
        def register_middleware(func):
            self._middlewares.append(func)
            return func

        @web.middleware
        @register_middleware
        async def authenticate(request: web.Request, handler):
            return await handler(request)
