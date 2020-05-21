from src.model.authentication.auth_data import AuthData


class AuthenticationResponseMapper:

    @staticmethod
    def map(auth_data: AuthData, user_info: object) -> dict:
        return {
            'role': auth_data.role,
            'id': getattr(user_info, 'id', None),
            'first_name': getattr(user_info, 'first_name', None),
            'last_name': getattr(user_info, 'last_name', None),
            'licence': getattr(user_info, 'licence', None),
            'specialties': getattr(user_info, 'specialties', None)
        }
