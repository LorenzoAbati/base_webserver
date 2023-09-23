from aiohttp import web
from service.entities.api.controller import Controller


class Api:

    def __init__(self, app):
        self._app = app

        self.controller = Controller(app=app)

    @property
    def middlewares(self):
        middlewares = []

        def register_middleware(func):
            middlewares.append(func)
            return func

        @web.middleware
        @register_middleware
        async def authenticate(request: web.Request, handler):
            return await handler(request)

        return middlewares
