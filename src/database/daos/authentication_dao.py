from src.database.daos.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.authentication.auth_data import AuthData


class AuthenticationDAO(GenericDAO):

    @classmethod
    async def find(cls, auth_data: AuthData) -> AuthData:
        """ Return auth data if existent """
        document = await cls.get_first({'_id': auth_data.user_id})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def add(cls, auth_data: AuthData):
        """ Should only be used by resource loader """
        await cls.insert(cls.__to_document(auth_data))

    @classmethod
    def __to_object(cls, document: dict) -> AuthData:
        return AuthData(
            user_id=document['_id'],
            password=document['password'],
            role=document['role'],
            device_id=document.get('device_id')
        )

    @classmethod
    def __to_document(cls, auth_data: AuthData) -> dict:
        return {
            '_id': auth_data.user_id,
            'password': auth_data.password,
            'role': auth_data.role
        }

    @classmethod
    def collection(cls):
        return Mongo.get().authentication
