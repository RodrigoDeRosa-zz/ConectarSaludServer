from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.authentication.authentication_service import AuthenticationService
from src.service.authentication.mappers.AuthenticationRequestMapper import AuthenticationRequestMapper
from src.service.authentication.mappers.AuthenticationResponseMapper import AuthenticationResponseMapper


class AuthenticationHandler(CustomRequestHandler):

    SUPPORTED_METHODS = ['GET']

    async def post(self):
        try:
            request = AuthenticationRequestMapper.map(self.__parse_body())
            auth_data = await AuthenticationService.authenticate(request)
            self.make_response(AuthenticationResponseMapper.map(auth_data))
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
