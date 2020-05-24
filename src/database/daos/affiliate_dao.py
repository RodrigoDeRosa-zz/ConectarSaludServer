from typing import List

from src.database.daos.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.affiliates.affiliate import Affiliate


class AffiliateDAO(GenericDAO):

    @classmethod
    async def find(cls, affiliate_dni: str) -> Affiliate:
        """ Return affiliate with given id if existent. """
        document = await cls.get_first({'_id': affiliate_dni})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def all(cls) -> List[Affiliate]:
        """ Returns all affiliate stored in the database. """
        documents = await cls.get_all()
        return [cls.__to_object(document) for document in documents]

    @classmethod
    async def store(cls, affiliate: Affiliate):
        """ Upsert affiliate in database. Creates if non existent, updates otherwise. """
        await cls.upsert(
            {'_id': affiliate.dni},
            {'$set': cls.__to_document(affiliate)}
        )

    @classmethod
    async def delete(cls, affiliate_dni: str):
        """ Remove affiliate from database. """
        await cls.delete_first({'_id': affiliate_dni})

    @classmethod
    def __to_object(cls, document: dict) -> Affiliate:
        return Affiliate(
            dni=document['_id'],
            first_name=document['first_name'],
            last_name=document['last_name'],
            plan=document['plan'],
            id=document['id']
        )

    @classmethod
    def __to_document(cls, affiliate: Affiliate) -> dict:
        document = dict()
        # Add only existent fields to the document. This way we can create and update with the same code
        if affiliate.first_name: document['first_name'] = affiliate.first_name
        if affiliate.last_name: document['last_name'] = affiliate.last_name
        if affiliate.plan: document['plan'] = affiliate.plan
        if affiliate.id: document['id'] = affiliate.id
        # Return create/update document
        return document

    @classmethod
    def collection(cls):
        return Mongo.get().affiliates
