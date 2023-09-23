import yaml
import os
from collections import namedtuple
from aiohttp import web
from service.entities.api import controller

# Define a Route named tuple to easily organize our routes
Route = namedtuple('Route', ['path', 'method', 'action'])

routes = []

try:
    # Load routes from YAML
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, 'routes.yaml'), 'r') as file:
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
        method = getattr(web, route.method.lower(), None)
        if not method:
            raise ValueError(f"Invalid HTTP method: {route.method}")

        action_callable = getattr(controller, route.action, None)
        if not action_callable:
            raise ValueError(f"Invalid action: {route.action}")

        aiohttp_routes.append(method(route.path, action_callable))

except FileNotFoundError:
    print("Error: routes.yaml file was not found!")
except yaml.YAMLError as e:
    print(f"Error parsing routes.yaml: {e}")
except ValueError as e:
    print(f"Error in routes configuration: {e}")
