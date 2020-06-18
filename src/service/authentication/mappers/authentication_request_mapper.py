from src.model.authentication.auth_data import AuthData
from src.model.errors.business_error import BusinessError


class AuthenticationRequestMapper:

    @staticmethod
    def map(request_body: dict) -> AuthData:
        # Check correctness of request
        for field in ['user_id', 'password']:
            if field not in request_body:
                raise BusinessError(f'Failed to map incoming request. Missing field with ID {field}', 400)
        # Do mapping
        return AuthData(
            user_id=request_body['user_id'],
            password=request_body['password'],
            device_id=request_body.get('token')
        )
