from src.handlers.custom_request_handler import CustomRequestHandler


class HealthCheckHandler(CustomRequestHandler):
    """ Handler for health checks. """

    SUPPORTED_METHODS = ['OPTIONS', 'GET']

    def get(self):
        self.set_status(200)

    def _log(self):
        # Avoid logging request data on health checks
        pass
