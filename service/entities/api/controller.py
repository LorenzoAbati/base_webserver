from aiohttp import web


class Controller:
    def __init__(self, app):
        self._app = app

        with open('res/index.html', 'r') as f:
            self.index_content = f.read()

    async def home_controller_index(self, request):
        # Serve the content directly from the variable
        return web.Response(text=self.index_content, content_type='text/html')

    async def auth_controller_show_login_form(self, request):
        pass

    async def auth_controller_do_login(self, request):
        # In real-world scenarios, you would handle login logic here.
        return web.Response(text="Auth Controller: Do Login Action")
