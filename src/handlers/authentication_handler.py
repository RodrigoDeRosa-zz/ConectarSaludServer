from src.database.daos.authentication_dao import AuthenticationDAO
from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.authentication.authentication_service import AuthenticationService
from src.service.authentication.mappers.authentication_request_mapper import AuthenticationRequestMapper
from src.service.authentication.mappers.authentication_response_mapper import AuthenticationResponseMapper


class AuthenticationHandler(CustomRequestHandler):

    SUPPORTED_METHODS = ['OPTIONS', 'POST', 'PUT']

    async def post(self):
        await self.wrap_handling(self.__authenticate, **{})

    async def put(self):
        """ TODO -> Remove this endpoint. """
        await AuthenticationDAO.insert(self._parse_body())
        self.make_response(self._parse_body())

    """ Handling methods """
    async def __authenticate(self):
        # Map JSON body to model object
        request = AuthenticationRequestMapper.map(self._parse_body())
        # Fetch needed information
        auth_data = await AuthenticationService.authenticate(request)
        # Map to JSON for response
        self.make_response(AuthenticationResponseMapper.map(auth_data))
