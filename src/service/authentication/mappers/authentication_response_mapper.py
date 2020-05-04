from src.model.authentication.auth_data import AuthData


class AuthenticationResponseMapper:

    @staticmethod
    def map(auth_data: AuthData) -> dict:
        return {'role': auth_data.role}
