from service.entities.api.api import Api
from service.entities.web.web_server import WebServer
from service.modules.besiness_manager import BusinessManager
from service.entities.database.database_manager import DatabaseManager


class ServiceApp:

    def __init__(self):
        self.database_manager = DatabaseManager(app=self)

        self.business_manager = BusinessManager(app=self)

        self.api = Api(app=self)

        WebServer(
            controller=self.api.controller,
            middlewares=self.api.middlewares
        ).run()

