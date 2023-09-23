import yaml
import os
import logging
from collections import namedtuple
import aiohttp
from typing import List
from service.entities.api.controller import Controller


logger = logging.getLogger(__name__)


class WebServer:
    def __init__(self,
                 controller: Controller,
                 host: str = None,
                 port: str = None,
                 middlewares: List[aiohttp.web_routedef.RouteDef] = None):

        self._port = '8080' if port is None else int(port)
        self._host = '127.0.0.1' if host is None else str(host)
        self._web = aiohttp.web.Application(middlewares=middlewares)

        self._init_server(controller)

    @property
    def port(self) -> str:
        """Get port where server is running"""
        return self._port

    @property
    def host(self) -> str:
        """Get the local IP address of the machine"""
        return self._host

    @property
    def socket(self) -> str:
        return f"{self._host}:{self._port}"

    def run(self):
        aiohttp.web.run_app(self._web, host=self._host, port=self._port)

    def _init_server(self, controller):
        routes = self._load_routes(controller)
        self._set_routes(routes)
        file_routes = self._load_file_routes()
        self._set_file_routes(file_routes)

    def _set_file_routes(self, file_routes) -> None:
        for file_route in file_routes:
            self._web.router.add_static(file_route.path, path=file_route.location)

    def _set_routes(self, routes: List[aiohttp.web_routedef.RouteDef]) -> None:
        self._web.add_routes(routes)

    def _load_file_routes(self):
        # Define a FileRoute named tuple to easily organize our file routes
        FileRoute = namedtuple('FileRoute', ['path', 'location'])

        file_routes = []

        try:
            # Load file routes from YAML
            dir_path = os.path.dirname(os.path.realpath(__file__))

            with open(os.path.join(dir_path, '../api/files.yaml'), 'r') as file:
                files_config = yaml.safe_load(file)

                # Validate the loaded configuration
                if not isinstance(files_config, dict) or "files" not in files_config:
                    raise ValueError("The files.yaml does not have the expected format.")

                for file_route in files_config["files"]:
                    if not all(key in file_route for key in ['path', 'location']):
                        raise ValueError(f"Missing keys in file route configuration: {file_route}")

                    file_routes.append(FileRoute(file_route["path"], file_route["location"]))

            logger.info("File routes added successfully")
            return file_routes

        except FileNotFoundError:
            logger.error("Error: files.yaml file was not found!")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing files.yaml: {e}")
        except ValueError as e:
            logger.error(f"Error in file routes configuration: {e}")

    def _load_routes(self, controller: Controller) -> aiohttp.web_routedef.RouteDef:
        # Define a Route named tuple to easily organize our routes
        Route = namedtuple('Route', ['path', 'method', 'action'])

        routes = []

        try:
            # Load routes from YAML
            dir_path = os.path.dirname(os.path.realpath(__file__))

            with open(os.path.join(dir_path, '../api/routes.yaml'), 'r') as file:
                routes_config = yaml.safe_load(file)

                # Validate the loaded configuration
                if not isinstance(routes_config, dict) or "routes" not in routes_config:
                    raise ValueError("The routes.yaml does not have the expected format.")

                for route in routes_config["routes"]:
                    if not all(key in route for key in ['path', 'method', 'action']):
                        raise ValueError(f"Missing keys in route configuration: {route}")

                    routes.append(Route(route["path"], route["method"], route["action"]))

            aiohttp_routes = []
            for route in routes:
                method = getattr(aiohttp.web, route.method.lower(), None)
                if not method:
                    raise ValueError(f"Invalid HTTP method: {route.method}")

                action_callable = getattr(controller, route.action, None)  # Changed this line
                if not action_callable:
                    raise ValueError(f"Invalid action: {route.action}")

                aiohttp_routes.append(method(route.path, action_callable))

            logger.info("Routes added successfully")
            return aiohttp_routes

        except FileNotFoundError:
            logger.error("Error: routes.yaml file was not found!")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing routes.yaml: {e}")
        except ValueError as e:
            logger.error(f"Error in routes configuration: {e}")
