from heapq import heappush, heappop

from typing import List, Optional

from src.model.consultations.consultation import QueueableData


class ConsultationQueue:

    def __init__(self, queue: List[QueueableData]):
        self.queue: List[QueueableData] = list()
        for element in queue:
            heappush(self.queue, element)

    def index_of(self, queueable_data: QueueableData):
        return self.queue.index(queueable_data)

    def __iter__(self):
        return list.__iter__(self.queue)

    def enqueue(self, queueable_data: QueueableData):
        """ Add consultation in priority queue. """
        heappush(self.queue, queueable_data)

    def dequeue(self) -> Optional[QueueableData]:
        """ Take next consultation. """
        try:
            return heappop(self.queue)
        except IndexError:
            return None

    def clear(self):
        """ Utility method """
        self.queue = []
