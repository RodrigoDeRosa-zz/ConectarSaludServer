from typing import Tuple

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.authentication_dao import AuthenticationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.model.authentication.auth_data import AuthData
from src.model.errors.business_error import BusinessError


class AuthenticationService:

    @classmethod
    async def authenticate(cls, auth_data: AuthData) -> Tuple[AuthData, object]:
        # Retrieve auth data from database
        fetched_data = await AuthenticationDAO.find(auth_data)
        # Check if user exists
        if not fetched_data:
            raise BusinessError(f'Unknown user with id {auth_data.user_id}', 404)
        # Validate password
        if fetched_data.password != auth_data.password:
            raise BusinessError(f'Invalid password for user {auth_data.user_id}', 413)
        if fetched_data.role == 'doctor':
            user_info = await DoctorDAO.find_by_dni(auth_data.user_id)
        elif fetched_data.role == 'affiliate':
            user_info = await AffiliateDAO.find(auth_data.user_id)
        else:
            # TODO -> This is for admin users
            user_info = None
        # Return related data found in database
        return fetched_data, user_info
