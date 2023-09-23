from aiohttp import web


class Controller:
    def __init__(self, app):
        self._app = app

    async def home_controller_index(self, request):
        return web.Response(text="Home Controller: Index Action")

    async def auth_controller_show_login_form(self, request):
        return web.Response(text="Auth Controller: Show Login Form Action")

    async def auth_controller_do_login(self, request):
        # In real-world scenarios, you would handle login logic here.
        return web.Response(text="Auth Controller: Do Login Action")
