from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.queue_dao import QueueDAO
from src.model.consultations.consultation import Consultation, QueueableData
from src.service.queue.consultation_queue import ConsultationQueue


class QueueManager:

    __QUEUE: ConsultationQueue = None

    @classmethod
    async def enqueue(cls, consultation: Consultation):
        """ Add consultation to queue. """
        if not cls.__QUEUE: await cls.__create_queue()
        queueable_data = cls.__to_queueable_data(consultation)
        # Store in memory
        cls.__QUEUE.enqueue(queueable_data)
        # Persist in DB
        await QueueDAO.store(queueable_data)

    @classmethod
    async def pop(cls) -> Consultation:
        """ Return the next consultation to be handled. """
        if not cls.__QUEUE: await cls.__create_queue()
        # Remove from memory and database
        queueable_data = cls.__QUEUE.dequeue()
        await QueueDAO.remove(queueable_data.id)
        # TODO -> Schedule new waiting time
        # Return related consultation object
        return await ConsultationDAO.find(queueable_data.id)

    @classmethod
    async def __create_queue(cls):
        """ Store all queueable data from database. """
        queue = await QueueDAO.all()
        cls.__QUEUE = ConsultationQueue(queue)

    @classmethod
    def __to_queueable_data(cls, consultation: Consultation) -> QueueableData:
        return QueueableData(
            id=consultation.id,
            creation_time=consultation.creation_date,
            priority=consultation.priority
        )
