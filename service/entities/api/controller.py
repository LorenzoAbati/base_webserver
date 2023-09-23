from aiohttp import web


# Define the action for the "/" route
async def home_controller_index(request):
    return web.Response(text="Home Controller: Index Action")


# Define the action to show the login form
async def auth_controller_show_login_form(request):
    return web.Response(text="Auth Controller: Show Login Form Action")


# Define the action to perform login
async def auth_controller_do_login(request):
    # In real-world scenarios, you would handle login logic here.
    return web.Response(text="Auth Controller: Do Login Action")
