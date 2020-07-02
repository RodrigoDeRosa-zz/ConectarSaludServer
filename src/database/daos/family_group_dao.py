from typing import List

from src.database.daos.generic_dao import GenericDAO
from src.database.mongo import Mongo


class FamilyGroupDAO(GenericDAO):

    @classmethod
    async def all(cls) -> List[str]:
        """ Returns all family groups stored in the database. """
        documents = await cls.get_all()
        return [document.get('members', list()) for document in documents]

    @classmethod
    async def store(cls, family_group: List[str]):
        """ Store new family group in database. """
        await cls.insert({'members': family_group})

    @classmethod
    def collection(cls):
        return Mongo.get().family_groups
