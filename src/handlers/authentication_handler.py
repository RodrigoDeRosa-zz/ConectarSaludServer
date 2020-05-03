from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.authentication.authentication_service import AuthenticationService
from src.service.authentication.mappers.AuthenticationRequestMapper import AuthenticationRequestMapper
from src.service.authentication.mappers.AuthenticationResponseMapper import AuthenticationResponseMapper


class AuthenticationHandler(CustomRequestHandler):

    SUPPORTED_METHODS = ['POST']

    async def post(self):
        try:
            # Map JSON body to model object
            request = AuthenticationRequestMapper.map(self._parse_body())
            # Fetch needed information
            auth_data = await AuthenticationService.authenticate(request)
            # Map to JSON for response
            self.make_response(AuthenticationResponseMapper.map(auth_data))
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
