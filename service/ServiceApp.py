from service.entities.api.api_manager import ApiManager
from service.modules.besiness_manager import BusinessManager
from service.entities.database.database_manager import DatabaseManager


class ServiceApp:

    def __init__(self):
        self.database_manager = DatabaseManager(app=self)

        self.business_manager = BusinessManager(app=self)

        self.api_manager = ApiManager(app=self)


