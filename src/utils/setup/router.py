from src.handlers.authentication_handler import AuthenticationHandler
from src.handlers.health_check_handler import HealthCheckHandler


class Router:

    # Dictionary to map route to Tornado RequestHandler subclasses
    ROUTES = {
        '/health/health-check': HealthCheckHandler,
        '/authenticate': AuthenticationHandler
    }

    @classmethod
    def get_routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
