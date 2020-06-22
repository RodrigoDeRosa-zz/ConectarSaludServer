from random import shuffle
from typing import Optional, Dict, List

from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.queue_dao import QueueDAO
from src.handlers.socket.socket_manager import SocketManager
from src.model.consultations.consultation import Consultation, QueueableData
from src.service.queue.consultation_queue import ConsultationQueue
from src.utils.scheduling.scheduler import Scheduler


class QueueManager:
    __QUEUES_BY_SPECIALTY: Dict[str, ConsultationQueue] = dict()
    CONSULTATION_MINUTES = 10
    __MAIN_QUEUE_ID = 'Medicina general'
    __PEDIATRICS = 'Pediatría'

    @classmethod
    async def enqueue(cls, consultation: Consultation):
        """ Add consultation to queue. """
        queueable_data = cls.__to_queueable_data(consultation)
        # Pediatrics should only be taken by a pediatrician
        queue_specialties = [cls.__PEDIATRICS] if cls.__PEDIATRICS in consultation.specialties \
            else set(consultation.specialties + [cls.__MAIN_QUEUE_ID])
        # Update every specialty's queue. Medicina general should always be included.
        for specialty in queue_specialties:
            # Create queue if not existent
            if specialty not in cls.__QUEUES_BY_SPECIALTY:
                cls.__QUEUES_BY_SPECIALTY[specialty] = await cls.__create_queue(specialty)
            # Store in memory
            cls.__QUEUES_BY_SPECIALTY[specialty].enqueue(queueable_data)
        # Persist in DB
        await QueueDAO.store(queueable_data)
        # Notify user approximate waiting time. Main queue is used for worst case scenario.
        time_queue_name = cls.__PEDIATRICS if cls.__PEDIATRICS in queue_specialties else cls.__MAIN_QUEUE_ID
        await cls.__notify_single_affiliate(
            queueable_data,
            cls.__QUEUES_BY_SPECIALTY[time_queue_name].index_of(queueable_data)
        )

    @classmethod
    async def pop(cls, specialties: List[str]) -> Optional[Consultation]:
        """ Return the next consultation to be handled from any of the given specialties. """
        shuffle(specialties)  # Shuffle to avoid getting always the same specialty
        for specialty in specialties:
            # Load queue if not existent in memory
            if specialty not in cls.__QUEUES_BY_SPECIALTY:
                cls.__QUEUES_BY_SPECIALTY[specialty] = await cls.__create_queue(specialty)
            # Pop event from memory queue
            queueable_data = cls.__QUEUES_BY_SPECIALTY[specialty].dequeue()
            # Go to the next specialty if there is no consultation to handle
            if not queueable_data: continue
            # Remove event from database
            await QueueDAO.remove(queueable_data.id)
            # Remove event from all of it's specialties queues
            for sub_specialty in set(queueable_data.specialties + [cls.__MAIN_QUEUE_ID]):
                if sub_specialty == specialty: continue
                cls.__QUEUES_BY_SPECIALTY[sub_specialty].remove(queueable_data)
            # Notify current affiliate that they're next
            await cls.__notify_single_affiliate(queueable_data)
            # Notify all enqueued affiliates of updated waiting time
            Scheduler.run_in_millis(cls.__notify_affiliates)
            # Return related consultation object
            return await ConsultationDAO.find(queueable_data.id)

    @classmethod
    async def cancel(cls, consultation: Consultation):
        """ Removes a consultation from the queue. """
        queueable_data = cls.__to_queueable_data(consultation)
        for specialty in set(queueable_data.specialties + [cls.__MAIN_QUEUE_ID]):
            # Load queue if not existent in memory
            if specialty not in cls.__QUEUES_BY_SPECIALTY:
                cls.__QUEUES_BY_SPECIALTY[specialty] = await cls.__create_queue(specialty)
            cls.__QUEUES_BY_SPECIALTY[specialty].remove(queueable_data)
            await QueueDAO.remove(queueable_data.id)

    @classmethod
    async def __notify_affiliates(cls):
        """ Send approximate remaining time to every affiliate via socket. """
        for index, value in enumerate(cls.__QUEUES_BY_SPECIALTY[cls.__MAIN_QUEUE_ID]):
            await cls.__notify_single_affiliate(value, index + 1)

    @classmethod
    async def __notify_single_affiliate(cls, queueable_data: QueueableData, index: int = 0):
        await SocketManager.notify_remaining_time(index * cls.CONSULTATION_MINUTES, queueable_data.socket_id)

    @classmethod
    async def __create_queue(cls, specialty: str) -> ConsultationQueue:
        """ Store all queueable data from database. """
        queue = await QueueDAO.all(specialty)
        return ConsultationQueue(queue)

    @classmethod
    def clear(cls):
        """ Utility method to clean memory queue. """
        for queue in cls.__QUEUES_BY_SPECIALTY.values():
            queue.clear()

    @classmethod
    def __to_queueable_data(cls, consultation: Consultation) -> QueueableData:
        return QueueableData(
            id=consultation.id,
            socket_id=consultation.socket_id,
            creation_time=consultation.creation_date,
            priority=consultation.priority,
            specialties=consultation.specialties
        )