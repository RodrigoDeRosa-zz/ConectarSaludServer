from src.database.daos.authentication_dao import AuthenticationDAO
from src.model.authentication.auth_data import AuthData
from src.model.errors.business_error import BusinessError


class AuthenticationService:

    @classmethod
    async def authenticate(cls, auth_data: AuthData) -> AuthData:
        # Retrieve auth data from database
        fetched_data = await AuthenticationDAO.find(auth_data)
        # Check if user exists
        if not fetched_data:
            raise BusinessError(f'Unknown user with id {auth_data.user_id}', 404)
        # Validate password
        if fetched_data.password != auth_data.password:
            raise BusinessError(f'Invalid password for user {auth_data.user_id}', 413)
        # Return related data found in database
        return fetched_data
