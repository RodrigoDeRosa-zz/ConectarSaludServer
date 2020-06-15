from typing import Optional

from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.queue_dao import QueueDAO
from src.handlers.socket.socket_manager import SocketManager
from src.model.consultations.consultation import Consultation, QueueableData
from src.service.queue.consultation_queue import ConsultationQueue
from src.utils.scheduling.scheduler import Scheduler


class QueueManager:

    __QUEUE: ConsultationQueue = None
    CONSULTATION_MINUTES = 10

    # TODO -> Take specialties into account

    @classmethod
    async def enqueue(cls, consultation: Consultation):
        """ Add consultation to queue. """
        if not cls.__QUEUE: await cls.__create_queue()
        queueable_data = cls.__to_queueable_data(consultation)
        # Store in memory
        cls.__QUEUE.enqueue(queueable_data)
        # Persist in DB
        await QueueDAO.store(queueable_data)
        # Notify user approximate waiting time
        await cls.__notify_single_affiliate(queueable_data, cls.__QUEUE.index_of(queueable_data))

    @classmethod
    async def pop(cls) -> Optional[Consultation]:
        """ Return the next consultation to be handled. """
        if not cls.__QUEUE: await cls.__create_queue()
        # Remove from memory and database
        queueable_data = cls.__QUEUE.dequeue()
        # Return None if there is no consultation to handle
        if not queueable_data: return None
        await QueueDAO.remove(queueable_data.id)
        # Notify current affiliate that they're next
        await cls.__notify_single_affiliate(queueable_data)
        # Notify all enqueued affiliates of updated waiting time
        Scheduler.run_in_millis(cls.__notify_affiliates)
        # Return related consultation object
        return await ConsultationDAO.find(queueable_data.id)

    @classmethod
    async def __notify_affiliates(cls):
        """ Send approximate remaining time to every affiliate via socket. """
        for index, value in enumerate(cls.__QUEUE):
            await cls.__notify_single_affiliate(value, index + 1)

    @classmethod
    async def __notify_single_affiliate(cls, queueable_data: QueueableData, index: int = 0):
        await SocketManager.notify_remaining_time(index * cls.CONSULTATION_MINUTES, queueable_data.socket_id)

    @classmethod
    async def __create_queue(cls):
        """ Store all queueable data from database. """
        queue = await QueueDAO.all()
        cls.__QUEUE = ConsultationQueue(queue)

    @classmethod
    def clear(cls):
        """ Utility method to clean memory queue. """
        cls.__QUEUE.clear()

    @classmethod
    def __to_queueable_data(cls, consultation: Consultation) -> QueueableData:
        return QueueableData(
            id=consultation.id,
            socket_id=consultation.socket_id,
            creation_time=consultation.creation_date,
            priority=consultation.priority
        )
