from dataclasses import dataclass
from datetime import datetime
from enum import Enum

@dataclass
class ConsultationOpinion:
    prescription: str = None
    indications: str = None


class ConsultationStatus(Enum):
    WAITING_DOCTOR = 'WAITING_DOCTOR'
    WAITING_CALL = 'WAITING_CALL'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


class ConsultationPriority(Enum):
    URGENT = 1
    COMMON = 0


@dataclass
class Consultation:
    id: str
    affiliate_dni: str
    creation_date: datetime
    status: ConsultationStatus = ConsultationStatus.WAITING_DOCTOR
    priority: ConsultationPriority = ConsultationPriority.COMMON
    doctor_id: str = None
    call_id: str = None
    score: float = None
    score_opinion: str = None
    prescription: str = None
    indications: str = None
    socket_id: str = None


@dataclass
class ConsultationScore:
    points: float
    opinion: str = None


@dataclass
class QueueableData:
    id: str
    socket_id: str
    creation_time: datetime
    priority: ConsultationPriority

    SECONDS_IN_MINUTE = 60
    PRIORITY_MINUTES = 30

    def __lt__(self, other):
        """ Used for priority queue ordering. Higher priority value means lower position in queue. """
        return self.priority_value() > other.priority_value()

    def priority_value(self) -> float:
        # Get the minutes this consultation has been waiting
        elapsed_minutes = (datetime.now() - self.creation_time).total_seconds() / self.SECONDS_IN_MINUTE
        # Each level of priority is equivalent to half an hour
        priority_equivalent_minutes = self.priority.value * self.PRIORITY_MINUTES
        # Total priority is the sum of both
        return elapsed_minutes + priority_equivalent_minutes
