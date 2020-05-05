from json import dumps, loads

from tornado.web import RequestHandler

from src.database.mongo import Mongo
from src.model.errors.business_error import BusinessError
from src.utils.mapping.mapping_utils import MappingUtils


class CustomRequestHandler(RequestHandler):

    INTERNAL_ERROR_MESSAGE = 'Internal Server Error. ' \
                             'Our best engineers were [probably] notified and are [probably] running to fix it.'

    def prepare(self):
        Mongo.set(self.settings['db'])

    def data_received(self, chunk):
        pass

    def make_error_response(self, status_code, message):
        """ Create a common error response. """
        self.set_status(status_code)
        response = {'status': status_code, 'message': message}
        self.write(response)

    def make_response(self, response=None, status_code=200):
        """ Create a common success response. """
        self.set_status(status_code)
        # Set default JSON header
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ', '.join(self.SUPPORTED_METHODS))
        # There are cases with no body
        if response:
            # The following is done to accept List responses (Tornado doesn't accept them by default)
            json_response = response if not isinstance(response, str) else loads(response)
            self.write(dumps(json_response))

    def options(self):
        self.make_response(status_code=200)

    def _parse_body(self):
        try:
            return MappingUtils.decode_request_body(self.request.body)
        except RuntimeError:
            raise BusinessError(f'Invalid request body {self.request.body}', 400)
