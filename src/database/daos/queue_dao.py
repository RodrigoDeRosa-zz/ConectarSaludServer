import pymongo
from typing import List

from src.database.daos.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.consultations.consultation import QueueableData


class QueueDAO(GenericDAO):

    @classmethod
    async def store(cls, queueable_data: QueueableData):
        """ Store the queueable data of a consultation """
        await cls.insert(cls.__to_document(queueable_data))

    @classmethod
    async def all(cls) -> List[QueueableData]:
        """ Returns all queueable data units stored in the database. """
        documents = await cls.get_all()
        return [cls.__to_object(document) for document in documents]

    @classmethod
    async def remove(cls, unit_id: str):
        """ Deletes the given queueable data unit. """
        await cls.delete_first({'_id': unit_id})

    @classmethod
    def __to_object(cls, document: dict) -> QueueableData:
        return QueueableData(
            id=document['_id'],
            socket_id=document['socket_id'],
            priority=document.get('priority', 0),
            creation_time=document['creation_time']
        )

    @classmethod
    def __to_document(cls, queueable_data: QueueableData) -> dict:
        return {
            '_id': queueable_data.id,
            'socket_id': queueable_data.socket_id,
            'priority': queueable_data.priority,
            'creation_time': queueable_data.creation_time,
        }

    @classmethod
    def create_indexes(cls, db):
        db.queue.create_index([('creation_time', pymongo.ASCENDING)])
        db.queue.create_index([('priority', pymongo.DESCENDING)])

    @classmethod
    def collection(cls):
        return Mongo.get().queue
