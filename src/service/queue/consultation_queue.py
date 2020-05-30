from heapq import heappush, heappop

from typing import List

from src.model.consultations.consultation import QueueableData


class ConsultationQueue:

    def __init__(self, queue: List[QueueableData]):
        self.queue = []
        for element in queue:
            heappush(self.queue, element)

    def enqueue(self, queueable_data: QueueableData):
        """ Add consultation in priority queue. """
        heappush(self.queue, queueable_data)

    def dequeue(self) -> QueueableData:
        """ Take next consultation. """
        return heappop(self.queue)
