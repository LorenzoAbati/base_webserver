from aiohttp import web
import aiofiles


class Controller:
    def __init__(self, app):
        self._app = app

    async def auth_controller_show_login_form(self, request):
        pass

    async def home_controller_index(self, request):
        async with aiofiles.open('res/index.html', mode='r') as f:
            content = await f.read()
        return web.Response(text=content, content_type='text/html')

    async def auth_controller_do_login(self, request):
        # In real-world scenarios, you would handle login logic here.
        return web.Response(text="Auth Controller: Do Login Action")
